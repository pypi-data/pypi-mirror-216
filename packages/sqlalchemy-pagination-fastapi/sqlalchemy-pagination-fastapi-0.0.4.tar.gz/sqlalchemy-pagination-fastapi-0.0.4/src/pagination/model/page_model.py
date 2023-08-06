import math

from typing import List, Generic, TypeVar
from pydantic import BaseModel
T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
