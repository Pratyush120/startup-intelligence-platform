from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    meta: Optional[dict[str, Any]] = None
    errors: Optional[list[str]] = None


def success_response(data: T = None, meta: dict = None) -> StandardResponse[T]:
    return StandardResponse(success=True, data=data, meta=meta, errors=None)


def error_response(errors: list[str]) -> StandardResponse[Any]:
    return StandardResponse(success=False, data=None, meta=None, errors=errors)
