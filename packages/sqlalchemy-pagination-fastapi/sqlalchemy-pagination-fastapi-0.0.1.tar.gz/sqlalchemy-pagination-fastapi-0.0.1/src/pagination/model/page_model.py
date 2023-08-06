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

    def __init__(self, items, page, page_size, total):
        super().__init__()
        self.items = items
        self.total = total
        self.page = page
        self.size = page_size
        self.pages = int(math.ceil(total / float(page_size)))
