class CommandError(Exception):
    """Command error."""


class RemoteError(Exception):
    """Remote error"""


class OfflineError(RemoteError):
    """Error to indicate host is offline."""


class SSHHostKeyUnknownError(RemoteError):
    """Error to indicate SSH host key is unknown."""


class SSHAuthError(RemoteError):
    """Error to indicate SSH authentication failed."""


class SSHConnectError(RemoteError):
    """Error to indicate SSH connection failed."""
