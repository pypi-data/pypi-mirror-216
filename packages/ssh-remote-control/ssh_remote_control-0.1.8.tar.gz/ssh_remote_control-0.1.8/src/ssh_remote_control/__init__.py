"""SSH remote control."""
from __future__ import annotations

import asyncio
import logging
from time import time

import async_timeout
import icmplib
import paramiko
import wakeonlan

from .collection import Collection
from .command import ActionCommand, Command, CommandOutput, SensorCommand
from .default_collections import ActionKey, SensorKey
from .errors import (
    CommandExecuteError,
    CommandFormatError,
    MACAdressUnavailableError,
    OfflineError,
    SSHAuthError,
    SSHConnectError,
    SSHHostKeyUnknownError,
)
from .event import Event
from .helpers import name_to_key
from .manager import DEFAULT_COMMAND_TIMEOUT, Manager
from .sensor import DynamicSensor, Sensor

_LOGGER = logging.getLogger(__name__)
_TEST_COMMAND = Command("")

DEFAULT_SSH_PORT = 22
DEFAULT_PING_TIMEOUT = 4
DEFAULT_SSH_TIMEOUT = 4
DEFAULT_ADD_HOST_KEYS = False
DEFAULT_ALLOW_TURN_OFF = False

IS_ONLINE = "is_online"
IS_CONNECTED = "is_connected"


class CustomRejectPolicy(paramiko.MissingHostKeyPolicy):
    """Custom reject policy for ssh client."""

    def missing_host_key(
        self, client: paramiko.SSHClient, hostname: str, key: paramiko.PKey
    ) -> None:
        raise SSHHostKeyUnknownError("Host key is unknown")


class State:
    """The State class."""

    is_online: bool = False
    is_connected: bool = False

    def __init__(self, remote: Remote) -> None:
        self._remote = remote
        self.on_change = Event()

    def update(self, name, value) -> None:
        """Update."""
        if getattr(self, name) == value:
            return

        setattr(self, name, value)
        self._remote.logger.info("%s: %s changed to %s", self._remote.name, name, value)
        self.on_change.notify(self)


class Remote(Manager):
    """The Remote class."""

    def __init__(
        self,
        host: str,
        *,
        name: str | None = None,
        mac_address: str | None = None,
        add_host_keys: bool = DEFAULT_ADD_HOST_KEYS,
        ssh_port: int = DEFAULT_SSH_PORT,
        ssh_user: str | None = None,
        ssh_password: str | None = None,
        ssh_key_file: str | None = None,
        ssh_host_keys_file: str | None = None,
        ssh_timeout: int = DEFAULT_SSH_TIMEOUT,
        ping_timeout: int = DEFAULT_PING_TIMEOUT,
        command_timeout: int = DEFAULT_COMMAND_TIMEOUT,
        collection: Collection | None = None,
        allow_turn_off: bool = DEFAULT_ALLOW_TURN_OFF,
        logger: logging.Logger = _LOGGER,
    ) -> None:
        super().__init__(
            name=name or host,
            command_timeout=command_timeout,
            collection=collection,
            logger=logger,
        )
        self.host = host
        self._mac_address = mac_address
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_key_file = ssh_key_file
        self.ssh_timeout = ssh_timeout
        self.ping_timeout = ping_timeout
        self.allow_turn_off = allow_turn_off
        self.state = State(self)
        self._ssh_client = paramiko.SSHClient()
        self._ssh_client.set_log_channel(self.logger.name)
        self._ssh_client.load_system_host_keys()
        self._ssh_client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy if add_host_keys else CustomRejectPolicy
        )

        if ssh_host_keys_file:
            with open(ssh_host_keys_file, "a", encoding="utf-8"):
                pass
            self._ssh_client.load_host_keys(ssh_host_keys_file)

    @property
    def hostname(self) -> str | None:
        """Hostname."""
        if sensor := self.sensors_by_key.get(SensorKey.HOSTNAME):
            return sensor.last_known_value

    @property
    def mac_address(self) -> str | None:
        """MAC address."""
        if self._mac_address:
            return self._mac_address
        if sensor := self.sensors_by_key.get(SensorKey.MAC_ADDRESS):
            return sensor.last_known_value

    @property
    def wol_support(self) -> bool | None:
        """Wake on LAN support."""
        if sensor := self.sensors_by_key.get(SensorKey.WOL_SUPPORT):
            return sensor.last_known_value

    @property
    def os_name(self) -> str | None:
        """OS name."""
        if sensor := self.sensors_by_key.get(SensorKey.OS_NAME):
            return sensor.last_known_value

    @property
    def os_version(self) -> str | None:
        """OS version."""
        if sensor := self.sensors_by_key.get(SensorKey.OS_VERSION):
            return sensor.last_known_value

    @property
    def machine_type(self) -> str | None:
        """Machine type."""
        if sensor := self.sensors_by_key.get(SensorKey.MACHINE_TYPE):
            return sensor.last_known_value

    def _execute_command_string(self, string: str) -> CommandOutput:
        if not self.state.is_connected:
            raise CommandExecuteError("Not connected")

        try:
            _, stdout_file, stderr_file = self._ssh_client.exec_command(
                string, timeout=float(self.ssh_timeout)
            )
        except Exception as exc:
            self._disconnect()
            raise CommandExecuteError("Disconnected during execution") from exc

        try:
            return CommandOutput(
                time(),
                [line.strip() for line in stdout_file.readlines()],
                [line.strip() for line in stderr_file.readlines()],
                stdout_file.channel.recv_exit_status(),
            )
        except Exception as exc:
            self._disconnect()
            raise CommandExecuteError("Disconnected after execution") from exc

    def _connect(self) -> None:
        if self.state.is_connected:
            return

        try:
            self._ssh_client.connect(
                self.host,
                self.ssh_port,
                self.ssh_user,
                self.ssh_password,
                key_filename=self.ssh_key_file,
                timeout=self.ssh_timeout,
                allow_agent=False,
            )
        except SSHHostKeyUnknownError:
            self._disconnect()
            raise
        except paramiko.AuthenticationException as exc:
            self._disconnect()
            raise SSHAuthError("SSH authentication failed") from exc
        except Exception as exc:
            self._disconnect()
            raise SSHConnectError("SSH connection failed") from exc

        self.state.update(IS_CONNECTED, True)

    def _disconnect(self) -> None:
        if not self.state.is_connected:
            return

        self._ssh_client.close()
        self.state.update(IS_CONNECTED, False)

        for command in self.sensor_commands:
            command.update_sensors(None)

    async def async_execute_command_string(
        self, string: str, command_timeout: int | None = None
    ) -> CommandOutput:
        loop = asyncio.get_running_loop()
        timeout = command_timeout or self.command_timeout

        try:
            async with async_timeout.timeout(timeout):
                return await loop.run_in_executor(
                    None, self._execute_command_string, string
                )
        except asyncio.TimeoutError as exc:
            raise CommandExecuteError(f"Timeout reached ({timeout} sec)") from exc

    async def async_connect(self) -> None:
        """Connect the SSH client.

        Set `state.is_connected` to `True` and update all
        sensor commands if successful, otherwise disconnect
        and raise an error.

        Raises:
            SSHHostKeyUnknownError
            SSHAuthError
            SSHConnectError
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._connect)

        for command in self.sensor_commands:
            try:
                await self.async_execute_command(command)
            except (CommandFormatError, CommandExecuteError):
                pass

    async def async_disconnect(self) -> None:
        """Disconnect the SSH client.

        Set `state.is_connected` to `False` and the
        sensor values of all sensor commands to `None`.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._disconnect)

    async def async_update_state(self, *, raise_errors: bool = False) -> None:
        """Update state.

        Raises:
            OfflineError (`raise_errors`)
            SSHHostKeyUnknownError
            SSHAuthError
            SSHConnectError (`raise_errors`)
        """
        if self.state.is_connected:
            try:
                await self.async_execute_command(_TEST_COMMAND)
                return
            except CommandExecuteError:
                pass

        try:
            host = await icmplib.async_ping(
                self.host,
                count=1,
                timeout=self.ping_timeout,
                privileged=False,
            )
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.info("%s: Ping request failed: %s", self.name, exc)
            self.state.update(IS_ONLINE, False)
        else:
            self.state.update(IS_ONLINE, host.is_alive)

        if not self.state.is_online:
            if raise_errors:
                raise OfflineError("Host is offline")
            return

        try:
            await self.async_connect()
        except SSHConnectError:
            if raise_errors:
                raise

    async def async_turn_on(self) -> None:
        """Turn the host on.

        Raises:
            MACAddressUnavailableError
        """
        if self.state.is_online:
            return

        if self.mac_address is None:
            raise MACAdressUnavailableError("MAC address is unavailable")

        wakeonlan.send_magic_packet(self.mac_address)

    async def async_turn_off(self) -> None:
        """Turn the host on.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        if self.allow_turn_off is False:
            return

        await self.async_run_action(ActionKey.TURN_OFF)
