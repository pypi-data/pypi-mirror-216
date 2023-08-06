from enum import Enum
from typing import Optional


class TapoError(Enum):
    INVALID_PUBLIC_KEY = -1010
    INVALID_CREDENTIAL = -1501
    INVALID_REQUEST = -1002
    INVALID_JSON = -1003


_error_message = {
    TapoError.INVALID_PUBLIC_KEY: "Invalid Public Key Length",
    TapoError.INVALID_CREDENTIAL: "Invalid credentials",
    TapoError.INVALID_REQUEST: "Invalid request",
    TapoError.INVALID_JSON: "Malformed json request"
}


class TapoException(Exception):
    error_code: int

    @staticmethod
    def from_error_code(error_code, msg: Optional[str]):
        try:
            tapo_error = TapoError(error_code)
            return TapoException(error_code, f"Returned error_code: {tapo_error}: {_error_message[tapo_error]}")
        except ValueError:
            return TapoException(error_code, f"Returned unknown error_code: {error_code}  msg: {msg}")

    def __init__(self, error_code, msg):
        super(TapoException, self).__init__(msg)
        self.error_code = error_code
