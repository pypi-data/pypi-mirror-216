import math

from .model.page_model import Page
from sqlalchemy.orm import Query


def paginate(query: Query, page: int, page_size: int):
    if page < 0:
        raise AttributeError('page needs to be >= 0')
    if page_size < 0:
        raise AttributeError('page_size needs to be >= 0')
    items = query.limit(page_size).offset(page * page_size).all()
    total = query.order_by(None).count()
    pages = int(math.ceil(total / float(page_size)))
    return Page(items=items, page=page, size=page_size, total=total, pages=pages)
