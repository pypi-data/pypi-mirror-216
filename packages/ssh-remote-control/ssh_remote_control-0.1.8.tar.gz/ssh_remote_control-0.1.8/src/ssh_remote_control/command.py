from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from string import Formatter
from time import time
from typing import TYPE_CHECKING

from .errors import CommandExecuteError, CommandFormatError
from .helpers import name_to_key
from .sensor import DynamicSensor, Sensor

if TYPE_CHECKING:
    from .manager import Manager

SENSOR_PLACEHOLDER_KEY = "_"


@dataclass(frozen=True)
class CommandOutput:
    """The CommandOutput class."""

    timestamp: float
    stdout: list[str] | None = None
    stderr: list[str] | None = None
    code: int | None = None


class Command:
    """The Command class."""

    def __init__(
        self,
        string: str,
        *,
        timeout: float | None = None,
        renderer: Callable[[str], str] | None = None,
    ) -> None:
        self.string = string
        self.timeout = timeout
        self.renderer = renderer

    @property
    def field_keys(self) -> list[str]:
        return {key for _, key, _, _ in Formatter().parse(self.string) if key}

    def get_context_keys(self, manager: Manager) -> set[str]:
        """Get context keys."""
        return {key for key in self.field_keys if key not in manager.sensors_by_key}

    def get_sensor_keys(self, manager: Manager) -> set[str]:
        """Get sensor keys."""
        return {key for key in self.field_keys if key in manager.sensors_by_key}

    async def async_format(self, manager: Manager, context: dict | None = None) -> str:
        """Format the string.

        Raises:
            CommandFormatError
        """
        context = context or {}
        sensor_keys = set()

        for key in self.get_context_keys(manager):
            if key not in context:
                raise CommandFormatError(f"Context key {key} is missing")

        for key in self.get_sensor_keys(manager):
            if key not in context:
                sensor = manager.get_sensor(key)
                if sensor.value is None:
                    sensor_keys.add(key)
                else:
                    context[key] = sensor.value

        for sensor in await manager.async_poll_sensors(sensor_keys):
            if sensor.value is None:
                raise CommandFormatError(f"Value of sensor {sensor.key} is None")
            context[sensor.key] = sensor.value

        string = self.string.format(**context)

        if self.renderer:
            try:
                string = self.renderer(string)
            except Exception as exc:
                raise CommandFormatError("Can't render command") from exc

        return string

    async def async_execute(
        self, manager: Manager, context: dict | None = None
    ) -> CommandOutput:
        """Execute.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        try:
            string = await self.async_format(manager, context)
        except CommandFormatError as exc:
            manager.logger.info("%s: %s -> %s", manager.name, self.string, exc)
            raise

        try:
            output = await manager.async_execute_command_string(string, self.timeout)
        except CommandExecuteError as exc:
            manager.logger.info("%s: %s -> %s", manager.name, string, exc)
            raise

        manager.logger.info(
            "%s: %s -> %s, %s, %s",
            manager.name,
            string,
            output.stdout,
            output.stderr,
            output.code,
        )

        return output


class ActionCommand(Command):
    """The ActionCommand class."""

    def __init__(
        self,
        string: str,
        name: str | None = None,
        key: str | None = None,
        *,
        timeout: float | None = None,
        renderer: Callable[[str], str] | None = None,
        options: dict | None = None,
    ) -> None:
        super().__init__(string, timeout=timeout, renderer=renderer)
        self.name = name
        self.key = key or name_to_key(name)
        self.options = options or {}


class SensorCommand(Command):
    """The SensorCommand class."""

    last_update: float | None = None

    def __init__(
        self,
        string: str,
        sensors: list[Sensor],
        *,
        timeout: float | None = None,
        renderer: Callable[[str], str] | None = None,
        interval: int | None = None,
    ) -> None:
        super().__init__(string, timeout=timeout, renderer=renderer)
        self.sensors = sensors
        self.interval = interval

    @property
    def sensors_by_key(self) -> dict[str, Sensor]:
        """Sensors by key."""
        result = {}
        for sensor in self.sensors:
            if sensor.key == SENSOR_PLACEHOLDER_KEY:
                continue
            result.update(
                {sensor.key: sensor, **sensor.child_sensors_by_key}
                if isinstance(sensor, DynamicSensor)
                else {sensor.key: sensor}
            )
        return result

    @property
    def dynamic_sensor(self) -> DynamicSensor | None:
        return next(
            (sensor for sensor in self.sensors if isinstance(sensor, DynamicSensor)),
            None,
        )

    @property
    def needs_update(self):
        """The command was never updated or reached its interval."""
        return self.last_update is None or (
            self.interval and time() - self.last_update >= self.interval
        )

    def remove_sensor(self, key: str) -> None:
        """Remove a sensor."""
        self.sensors = [
            Sensor(key=SENSOR_PLACEHOLDER_KEY) if sensor.key == key else sensor
            for sensor in self.sensors
        ]

    def update_sensors(self, output: CommandOutput | None) -> None:
        """Update sensors."""
        if output and output.code == 0:
            self.last_update = output.timestamp
            data = output.stdout
        else:
            data = None

        if dynamic_sensor := self.dynamic_sensor:
            dynamic_sensor.update(data)
            return

        if data is None:
            data = []

        for i, sensor in enumerate(self.sensors):
            sensor.update(data[i] if len(data) > i else None)

    async def async_execute(
        self, manager: Manager, context: dict | None = None
    ) -> CommandOutput:
        try:
            output = await super().async_execute(manager, context)
        except (CommandFormatError, CommandExecuteError):
            self.update_sensors(None)
            raise

        self.update_sensors(output)

        return output
