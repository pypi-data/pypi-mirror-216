# lib
from pydantic import BaseModel
from typing import Type
import math

# fastapi
from fastapi import HTTPException

# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query

# app
from hipal_mixin_scrud.schemas.paginate_params import PaginateParams


class ListModelMixin:
    """
    List a queryset.
    """

    Base = declarative_base()

    def paginate(
        self,
        db_session: Session,
        model: Type[Base],
        squema: BaseModel,
        path: str,
        paginate_params: PaginateParams = PaginateParams(),
        query_model: Query = None,
    ):

        query = db_session.query(model) if query_model is None else query_model

        if paginate_params.offset < 0:
            raise HTTPException(
                status_code=400,
                detail="Offset debe ser positivo.",
            )

        if paginate_params.limit < 1:
            raise HTTPException(
                status_code=400,
                detail="Limite debe ser mayor que 0.",
            )

        if paginate_params.search:
            SEPARATOR = ";"
            OPERATOR = "="

            filters = paginate_params.search.split(SEPARATOR)
            filters_sql = []

            for filter in filters:
                field = filter.split(OPERATOR)[0]
                field = getattr(model, field)
                search_value = filter.split(OPERATOR)[1]

                filter = cast(field, String).ilike(f"%{search_value}%")

                filters_sql.append(filter)

            query = query.filter(or_(*filters_sql))

        order_by = None
        
        if hasattr(model, "created_at"):
            order_by = getattr(model, "created_at")
            order_by = order_by.desc()

        if paginate_params.sort:
            order_by = getattr(model, paginate_params.sort_field)
            order_by = getattr(order_by, paginate_params.sort.value)()

        query = query.order_by(order_by)
        paginate_model = query.limit(paginate_params.limit).offset(
            paginate_params.offset
        )
        total_pages = math.ceil(query.count() / paginate_params.limit)
        total_items = query.count()

        obj = {
            "pagination": {
                "offset": paginate_params.offset,
                "limit": paginate_params.limit,
                "total": total_items,
                "total_pages": total_pages,
                "links": {
                    "first": (f"{path}?" f"offset=0&limit={paginate_params.limit}"),
                    "prev": (
                        f"{path}?"
                        f"offset={paginate_params.offset-paginate_params.limit}"
                        f"&limit={paginate_params.limit}"
                    ),
                    "next": (
                        f"{path}"
                        f"?offset={paginate_params.offset+paginate_params.limit}"
                        f"&limit={paginate_params.limit}"
                    ),
                    "last": (
                        f"{path}"
                        f"?offset={total_pages}"
                        f"&limit={paginate_params.limit}"
                    ),
                },
            },
            "data": [squema.from_orm(row) for row in paginate_model.all()],
        }
        
        return obj
