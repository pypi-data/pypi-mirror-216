from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import KW_ONLY, dataclass, field
import logging
import re
from typing import TYPE_CHECKING, Any

from .event import Event
from .helpers import name_to_key

if TYPE_CHECKING:
    from .command import Command
    from .manager import Manager

_LOGGER = logging.getLogger(__name__)

TRUE_STRINGS = ["true", "enabled", "on", "active", "1"]
FALSE_STRINGS = ["false", "disabled", "off", "inactive", "0"]


@dataclass
class Sensor:
    """The Sensor class."""

    name: str | None = None
    key: str | None = None
    _: KW_ONLY
    dynamic: bool | None = None
    separator: str | None = None
    unit: str | None = None
    renderer: Callable[[str], str] | None = None
    command_set: Command | None = None
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        self.id = None
        self.key = self.key or name_to_key(self.name)
        self.value: Any | None = None
        self.last_known_value: Any | None = None
        self.child_sensors: list[Sensor] = []
        self.on_update = Event()
        self.on_child_added = Event()
        self.on_child_removed = Event()

    @property
    def is_dynamic(self) -> bool:
        """Is dynamic."""
        return self.dynamic is True

    @property
    def is_controllable(self) -> bool:
        """Is controllable."""
        return self.command_set is not None

    @property
    def child_sensors_by_key(self) -> dict[str, Sensor]:
        """Child sensors by key."""
        return {child.key: child for child in self.child_sensors}

    def _get_control_command(self, _: Any) -> Command | None:
        return self.command_set

    def _add_child(self, child: Sensor) -> None:
        self.child_sensors.append(child)
        self.on_child_added.notify(self, child)

    def _remove_child(self, child: Sensor) -> None:
        self.child_sensors.remove(child)
        self.on_child_removed.notify(self, child)

    def _render(self, value_string: str) -> str:
        if self.renderer:
            return self.renderer(value_string)

        return value_string

    def _validate(self, value: Any) -> None:
        if value is None:
            raise ValueError("Value is None")

    def _update_value(self, data: str | None) -> None:
        if data is None:
            self.value = None
            return

        try:
            value = self._render(data)
        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.warning("%s: Render error: %s (%s)", self.key, exc, data)
            self.value = None
            return

        try:
            self._validate(value)
        except (TypeError, ValueError) as exc:
            _LOGGER.warning("%s: Validate error: %s (%s)", self.key, exc, value)
            self.value = None
            return

        self.value = self.last_known_value = value

    def _update_child_sensors(self, data: list[str] | None) -> None:
        if data is None:
            for child in self.child_sensors:
                child.update(None)
            return

        dynamic_data_list = [
            DynamicData(self.name, self.key, *(field.strip() for field in row))
            for row in (line.split(self.separator, 2) for line in data)
            if len(row) >= 2
        ]

        dynamic_data_by_key = {
            dynamic_data.key: dynamic_data for dynamic_data in dynamic_data_list
        }

        for key, dynamic_data in dynamic_data_by_key.items():
            if key not in self.child_sensors_by_key:
                child = deepcopy(self)
                child.id = dynamic_data.id
                child.key = dynamic_data.key
                child.name = dynamic_data.name
                child.dynamic = False
                self._add_child(child)

        for child in self.child_sensors:
            if child.key in dynamic_data_by_key:
                dynamic_data = dynamic_data_by_key[child.key]
                child.update(dynamic_data.value_string)
            else:
                self._remove_child(child)

    def update(self, data: Any) -> None:
        """Update and notify `on_update` subscribers."""
        if self.is_dynamic:
            self.value = self.last_known_value = None
            self._update_child_sensors(data)
        else:
            self.child_sensors = []
            self._update_value(data)

        self.on_update.notify(self)

    async def async_set(self, manager: Manager, value: Any) -> None:
        """Set.

        Raises:
            TypeError
            ValueError
            CommandFormatError
            CommandExecuteError
        """
        self._validate(value)
        command = self._get_control_command(value)

        if command is None or value == self.value:
            return

        await manager.async_execute_command(
            command, context={"id": self.id, "value": value}
        )


@dataclass
class TextSensor(Sensor):
    """The TextSensor class."""

    _: KW_ONLY
    minimum: int | None = None
    maximum: int | None = None
    pattern: str | None = None

    def _validate(self, value: Any) -> None:
        super()._validate(value)

        if not isinstance(value, str):
            raise TypeError(f"Value is {type(value)} and not {str}")

        if self.minimum and len(value) < self.minimum:
            raise ValueError(f"Value is shorter then {self.minimum}")

        if self.maximum and len(value) > self.maximum:
            raise ValueError(f"Value is longer then {self.maximum}")

        if self.pattern and not re.fullmatch(self.pattern, value):
            raise ValueError(f"Value doesn't match {self.pattern}")


@dataclass
class NumberSensor(Sensor):
    """The NumberSensor class."""

    _: KW_ONLY
    minimum: float | None = None
    maximum: float | None = None

    def _render(self, value_string: str) -> float:
        value_string = super()._render(value_string)
        return float(value_string)

    def _validate(self, value: Any) -> None:
        super()._validate(value)

        if not isinstance(value, float):
            raise TypeError(f"Value is {type(value)} and not {float}")

        if self.minimum and value < self.minimum:
            raise ValueError(f"Value is smaller then {self.minimum}")

        if self.maximum and value > self.maximum:
            raise ValueError(f"Value is bigger then {self.maximum}")


@dataclass
class BinarySensor(Sensor):
    """The BinarySensor class."""

    _: KW_ONLY
    command_on: Command | None = None
    command_off: Command | None = None
    payload_on: str | None = None
    payload_off: str | None = None

    @property
    def is_controllable(self) -> bool:
        if self.command_on and self.command_off:
            return True

        return self.command_set is not None

    def _get_control_command(self, value: Any) -> Command | None:
        if self.command_on and value is True:
            return self.command_on

        if self.command_off and value is False:
            return self.command_off

        return self.command_set

    def _render(self, value_string: str) -> bool:
        value_string = super()._render(value_string)

        if self.payload_on:
            if value_string == self.payload_on:
                return True
            if not self.payload_off:
                return False

        if self.payload_off:
            if value_string == self.payload_off:
                return False
            if not self.payload_on:
                return True

        if value_string.lower() in TRUE_STRINGS:
            return True

        if value_string.lower() in FALSE_STRINGS:
            return False

        raise ValueError("Can't generate boolean from string")

    def _validate(self, value: Any) -> None:
        super()._validate(value)

        if not isinstance(value, bool):
            raise TypeError(f"Value is {type(value)} and not {bool}")


class DynamicData:
    """The DynamicData class."""

    def __init__(
        self,
        parent_name: str | None,
        parent_key: str,
        data_id: str,
        data_value_string: str,
        data_name: str | None = None,
    ) -> None:
        name = data_name or data_id
        self.id = data_id
        self.key = f"{parent_key}_{name_to_key(name)}"
        self.name = f"{parent_name} {name}" if parent_name else name
        self.value_string = data_value_string
