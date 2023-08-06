class OfflineError(Exception):
    """Error to indicate host is offline."""


class SSHAuthError(Exception):
    """Error to indicate SSH authentication failed."""


class SSHConnectError(Exception):
    """Error to indicate SSH connection failed."""


class SSHHostKeyUnknownError(Exception):
    """Error to indicate SSH host key is unknown."""


class CommandFormatError(Exception):
    """Error to indicate command formatting failed."""


class CommandExecuteError(Exception):
    """Error to indicate command execution failed."""


class MACAdressUnavailableError(Exception):
    """Error to indicate MAC address is unavailable."""
