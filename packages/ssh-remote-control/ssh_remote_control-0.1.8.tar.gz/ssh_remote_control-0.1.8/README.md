# SSH Remote Control

## Initialize

```python
from ssh_remote_control import Remote

remote = Remote("192.168.0.123", ssh_user="user", ssh_password="1234")

# Will raise an error if the host is not online or the SSH connection fails
await remote.async_update_state(validate=True)

# Check the remote state
remote.state.is_online
remote.state.is_connected
```

## Initialize with a command set

```python
from ssh_remote_control.default_command_sets import linux, ServiceKey, SensorKey

remote = Remote("192.168.0.123", ssh_user="user", ssh_password="1234", command_set=linux)

await remote.async_update_state(validate=True)

# Get the value of a sensor
remote.get_sensor(SensorKey.CPU_LOAD).value

# Call a service
await remote.async_call_service(ServiceKey.RESTART)
```

## Execute a command

```python
from ssh_remote_control import Command

output = await remote.async_execute(Command("echo Hello from host"))
output.stdout
```
