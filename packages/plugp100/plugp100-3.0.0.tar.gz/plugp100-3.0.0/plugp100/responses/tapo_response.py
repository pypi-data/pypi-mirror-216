from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Any

from plugp100.responses.tapo_exception import TapoException
from plugp100.common.functional.either import Either, Right, Left

T = TypeVar("T")


@dataclass
class TapoResponse(Generic[T]):
    error_code: int
    result: Optional[T]
    msg: Optional[str]

    @staticmethod
    def from_json(json: dict[str, Any]) -> 'TapoResponse[dict[str, Any]]':
        return TapoResponse(
            json.get('error_code', -1),
            json.get('result', {}),
            json.get('msg', 'No message')
        )

    def validate(self) -> Either['TapoResponse[T]', Exception]:
        if self.error_code == 0:
            return Right(self)
        else:
            return Left(TapoException.from_error_code(self.error_code, self.msg))
