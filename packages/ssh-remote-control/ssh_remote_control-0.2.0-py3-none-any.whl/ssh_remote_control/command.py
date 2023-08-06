from __future__ import annotations

from collections.abc import Callable
from dataclasses import KW_ONLY, dataclass, field
from string import Formatter
from typing import TYPE_CHECKING

from .errors import CommandExecuteError, CommandFormatError
from .helpers import name_to_key
from .sensor import Sensor

if TYPE_CHECKING:
    from .manager import CommandOutput, Manager

SENSOR_PLACEHOLDER_KEY = "_"


@dataclass
class Command:
    """The Command class."""

    string: str
    _: KW_ONLY
    timeout: float | None = None
    renderer: Callable[[str], str] | None = None

    @property
    def field_keys(self) -> list[str]:
        """Field keys."""
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


@dataclass
class ActionCommand(Command):
    """The ActionCommand class."""

    name: str | None = None
    key: str | None = None
    _: KW_ONLY
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        self.key = self.key or name_to_key(self.name)


@dataclass
class SensorCommand(Command):
    """The SensorCommand class."""

    sensors: list[Sensor] = field(default_factory=list)
    _: KW_ONLY
    interval: int | None = None

    def __post_init__(self):
        self.last_update: float | None = None

    @property
    def sensors_by_key(self) -> dict[str, Sensor]:
        """Sensors by key."""
        return {
            sensor.key: sensor
            for command_sensor in self.sensors
            for sensor in (command_sensor, *command_sensor.child_sensors)
            if command_sensor.key != SENSOR_PLACEHOLDER_KEY
        }

    @property
    def dynamic_sensor(self) -> Sensor | None:
        return next(
            (sensor for sensor in self.sensors if sensor.is_dynamic),
            None,
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
