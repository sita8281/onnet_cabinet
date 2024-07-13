class DeilError(Exception):
    pass


class AuthFailed(DeilError):
    pass


class TimeoutResponse(DeilError):
    pass


class ParsingError(DeilError):
    pass

