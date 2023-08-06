from __future__ import annotations

from collections.abc import Callable
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


def _string_to_bool(
    payload_on: str | None, payload_off: str | None, string: str
) -> bool | None:
    if payload_on:
        if string == payload_on:
            return True
        if not payload_off:
            return False

    if payload_off:
        if string == payload_off:
            return False
        if not payload_on:
            return True

    if string.lower() in TRUE_STRINGS:
        return True

    if string.lower() in FALSE_STRINGS:
        return False


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


class Sensor:
    """The Sensor class."""

    value: Any | None = None
    last_known_value: Any | None = None

    def __init__(
        self,
        name: str | None = None,
        key: str | None = None,
        child_id: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_min: int | float | None = None,
        value_max: int | float | None = None,
        value_pattern: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        command_set: Command | None = None,
        command_on: Command | None = None,
        command_off: Command | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        self.name = name
        self.key = key or name_to_key(name)
        self.child_id = child_id
        self.value_type = value_type or str
        self.value_unit = value_unit
        self.value_min = value_min
        self.value_max = value_max
        self.value_pattern = value_pattern
        self.value_renderer = value_renderer
        self.command_set = command_set
        self.command_on = command_on
        self.command_off = command_off
        self.payload_on = payload_on
        self.payload_off = payload_off
        self.options = options or {}
        self.on_update = Event()

    @property
    def is_controllable(self) -> bool:
        """Return `True` if `async_set` is available."""
        if self.value_type == bool and self.command_on and self.command_off:
            return True

        return self.command_set is not None

    def _render(self, value_string: str) -> Any:
        if self.value_renderer:
            value_string = self.value_renderer(value_string)

        if self.value_type is bool:
            return _string_to_bool(self.payload_on, self.payload_off, value_string)

        if self.value_type is int:
            return int(float(value_string))

        return self.value_type(value_string)

    def _validate(self, value: Any) -> bool:
        if not isinstance(value, self.value_type):
            raise TypeError(f"Value is {type(value)} and not {self.value_type}")

        if self.value_type == str:
            if self.value_min and len(value) < self.value_min:
                raise ValueError(f"Value is shorter then {self.value_min} characters")
            if self.value_max and len(value) > self.value_max:
                raise ValueError(f"Value is longer then {self.value_min} characters")
            if self.value_pattern and not re.fullmatch(self.value_pattern, value):
                raise ValueError(f"Value doesn't match {self.value_pattern}")

        if self.value_type in [int, float]:
            if self.value_min and value < self.value_min:
                raise ValueError(f"Value is smaller then {self.value_min}")
            if self.value_max and value > self.value_max:
                raise ValueError(f"Value is bigger then {self.value_min}")

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

    def update(self, data: Any | None) -> None:
        """Update value and notify `on_update` subscribers."""
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
        if not self.is_controllable or value == self.value:
            return

        self._validate(value)

        if self.value_type == bool and self.command_on and self.command_off:
            command = self.command_on if value else self.command_off
        else:
            command = self.command_set

        await manager.async_execute_command(
            command, context={"id": self.child_id, "value": value}
        )


class DynamicSensor(Sensor):
    """The DynamicSensor class."""

    value: list[Sensor]

    def __init__(
        self,
        name: str | None = None,
        key: str | None = None,
        *,
        separator: str | None = None,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_min: int | float | None = None,
        value_max: int | float | None = None,
        value_pattern: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        command_set: Command | None = None,
        command_on: str | None = None,
        command_off: str | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        super().__init__(
            name,
            key,
            value_type=value_type,
            value_unit=value_unit,
            value_min=value_min,
            value_max=value_max,
            value_pattern=value_pattern,
            value_renderer=value_renderer,
            command_set=command_set,
            command_on=command_on,
            command_off=command_off,
            payload_on=payload_on,
            payload_off=payload_off,
            options=options,
        )
        self.separator = separator
        self.value = []
        self.on_child_added = Event()
        self.on_child_removed = Event()

    @property
    def child_sensors_by_key(self) -> dict[str, Sensor]:
        """Child sensors by key."""
        return {child.key: child for child in self.value}

    def _create_child(self, dynamic_data: DynamicData) -> Sensor:
        return Sensor(
            dynamic_data.name,
            dynamic_data.key,
            dynamic_data.id,
            value_type=self.value_type,
            value_unit=self.value_unit,
            value_min=self.value_min,
            value_max=self.value_max,
            value_renderer=self.value_renderer,
            command_set=self.command_set,
            command_on=self.command_on,
            command_off=self.command_off,
            payload_on=self.payload_on,
            payload_off=self.payload_off,
            options=self.options,
        )

    def _add_child(self, child: Sensor) -> None:
        self.value.append(child)
        self.on_child_added.notify(self, child)

    def _remove_child(self, child: Sensor) -> None:
        if child.value is not None:
            child.update(None)
        self.value.remove(child)
        self.on_child_removed.notify(self, child)

    def _update_value(self, data: list[str] | None) -> None:
        if data is None:
            for child in self.value:
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
                new_child = self._create_child(dynamic_data)
                self._add_child(new_child)

        for child in self.value:
            if child.key in dynamic_data_by_key:
                dynamic_data = dynamic_data_by_key[child.key]
                child.update(dynamic_data.value_string)
            else:
                self._remove_child(child)

    async def async_set(self, manager: Manager, value: Any) -> None:
        for child in self.value:
            await child.async_set(manager, value)
