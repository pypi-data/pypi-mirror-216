from ..collection import Collection
from ..command import ActionCommand, SensorCommand
from ..sensor import DynamicSensor, Sensor
from .const import ActionKey, ActionName, SensorKey, SensorName

linux = Collection(
    "Linux",
    [
        ActionCommand(
            "/sbin/shutdown -h now",
            ActionName.TURN_OFF,
            ActionKey.TURN_OFF,
        ),
        ActionCommand(
            "/sbin/shutdown -r now",
            ActionName.RESTART,
            ActionKey.RESTART,
        ),
    ],
    [
        SensorCommand(
            "cat /sys/class/net/{interface}/address",
            [
                Sensor(
                    SensorName.MAC_ADDRESS,
                    SensorKey.MAC_ADDRESS,
                )
            ],
        ),
        SensorCommand(
            "cat /sys/class/net/{interface}/device/power/wakeup",
            [
                Sensor(
                    SensorName.WOL_SUPPORT,
                    SensorKey.WOL_SUPPORT,
                    value_type=bool,
                    payload_on="enabled",
                )
            ],
        ),
        SensorCommand(
            "/sbin/route -n | awk '($1 == \"0.0.0.0\") {{print $NF; exit}}'",
            [
                Sensor(
                    SensorName.INTERFACE,
                    SensorKey.INTERFACE,
                )
            ],
        ),
        SensorCommand(
            "uname -a | awk '{{print $1; print $3; print $2; print $(NF-1);}}'",
            [
                Sensor(
                    SensorName.OS_NAME,
                    SensorKey.OS_NAME,
                ),
                Sensor(
                    SensorName.OS_VERSION,
                    SensorKey.OS_VERSION,
                ),
                Sensor(
                    SensorName.HOSTNAME,
                    SensorKey.HOSTNAME,
                ),
                Sensor(
                    SensorName.MACHINE_TYPE,
                    SensorKey.MACHINE_TYPE,
                ),
            ],
        ),
        # TODO: OS_ARCHITECTURE
        SensorCommand(
            "free -m | awk 'tolower($0)~/mem/ {{print $2}}'",
            [
                Sensor(
                    SensorName.TOTAL_MEMORY,
                    SensorKey.TOTAL_MEMORY,
                    value_type=int,
                    value_unit="MB",
                )
            ],
        ),
        SensorCommand(
            "free -m | awk 'tolower($0)~/mem/ {{print $4}}'",
            [
                Sensor(
                    SensorName.FREE_MEMORY,
                    SensorKey.FREE_MEMORY,
                    value_type=int,
                    value_unit="MB",
                )
            ],
            interval=30,
        ),
        SensorCommand(
            "df -m | awk '/^\\/dev\\// {{print $6 \"|\" $4}}'",
            [
                DynamicSensor(
                    SensorName.FREE_DISK_SPACE,
                    SensorKey.FREE_DISK_SPACE,
                    value_type=int,
                    value_unit="MB",
                    separator="|",
                )
            ],
            interval=300,
        ),
        SensorCommand(
            "top -bn1 | head -n3 | awk 'tolower($0)~/cpu/ "
            + "{{for(i=1;i<NF;i++){{if(tolower($i)~/cpu/)"
            + "{{idle=$(i+7); print 100-idle;}}}}}}'",
            [
                Sensor(
                    SensorName.CPU_LOAD,
                    SensorKey.CPU_LOAD,
                    value_type=int,
                    value_unit="%",
                )
            ],
            interval=30,
        ),
        SensorCommand(
            "echo $(($(cat /sys/class/thermal/thermal_zone0/temp) / 1000))",
            [
                Sensor(
                    SensorName.TEMPERATURE,
                    SensorKey.TEMPERATURE,
                    value_type=int,
                    value_unit="°C",
                )
            ],
            interval=60,
        ),
    ],
)
