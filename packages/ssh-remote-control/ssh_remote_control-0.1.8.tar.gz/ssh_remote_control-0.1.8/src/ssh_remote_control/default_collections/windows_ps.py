from ..collection import Collection
from ..command import ActionCommand, SensorCommand
from ..sensor import DynamicSensor, Sensor
from .const import ActionKey, ActionName, SensorKey, SensorName

windows_ps = Collection(
    "Windows (Power Shell)",
    [
        ActionCommand(
            "Stop-Computer -Force",
            ActionName.TURN_OFF,
            ActionKey.TURN_OFF,
        ),
        ActionCommand(
            "Restart-Computer -Force",
            ActionName.RESTART,
            ActionKey.RESTART,
        ),
    ],
    [
        # TODO: MAC_ADDRESS
        # TODO: WOL_SUPPORT
        # TODO: INTERFACE
        SensorCommand(
            "$x = Get-CimInstance Win32_ComputerSystem | "
            + "Select Name, SystemType;"
            + "$x.Name;"
            + "$x.SystemType;",
            [
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
        SensorCommand(
            "$x = Get-CimInstance Win32_OperatingSystem | "
            + "Select Caption, Version, OSArchitecture;"
            + "$x.Caption;"
            + "$x.Version;"
            + "$x.OSArchitecture;",
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
                    SensorName.OS_ARCHITECTURE,
                    SensorKey.OS_ARCHITECTURE,
                ),
            ],
        ),
        SensorCommand(
            "$x = Get-CimInstance Win32_ComputerSystem | "
            + "Select TotalPhysicalMemory;"
            + "[math]::Round($x.TotalPhysicalMemory/1MB);",
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
            "$x = Get-CimInstance Win32_OperatingSystem | "
            + "Select FreePhysicalMemory;"
            + "[math]::Round($x.FreePhysicalMemory/1KB);",
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
            "Get-CimInstance Win32_LogicalDisk | "
            + "Select DeviceID, FreeSpace | ForEach-Object "
            + '{{$_.DeviceID+"|"+[math]::Round($_.FreeSpace/1MB)}}',
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
            "$x = Get-CimInstance Win32_Processor | "
            + "Select LoadPercentage;"
            + "$x.LoadPercentage;",
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
            "$x = Get-CimInstance msacpi_thermalzonetemperature "
            + '-namespace "root/wmi" | '
            + "Select CurrentTemperature;"
            + "($x.CurrentTemperature - 2732) / 10;",
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
