
class MissingTokenError(Exception):
    pass


class ExpiredSignatureError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class WrongPasswordError(Exception):
    pass