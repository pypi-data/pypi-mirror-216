from typing import Generic, TypeVar

from pydantic import AnyHttpUrl, Field
from pydantic.generics import GenericModel


M = TypeVar('M')


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field()
    next: AnyHttpUrl | None
    previous: AnyHttpUrl | None
    results: list[M] = Field()
