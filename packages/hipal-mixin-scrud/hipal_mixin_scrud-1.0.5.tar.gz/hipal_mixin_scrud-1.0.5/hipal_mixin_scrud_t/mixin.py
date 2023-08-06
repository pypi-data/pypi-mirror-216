from fastapi import Depends, HTTPException, Request, Response
from typing import Any, Callable, Dict, List, Optional, Sequence, TypeVar
from typing import Type
from pydantic import BaseModel
from types import FunctionType
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from crud.generator import MixinGenerator
from crud.mixin_list import ListModelMixin
from schemas.paginate_params import PaginateParams
from sqlalchemy.ext.declarative import DeclarativeMeta as Model

T = TypeVar("T", bound=BaseModel)
DEPENDENCIES = Optional[Sequence[Depends]]


class MixinCrud(MixinGenerator, ListModelMixin):
    """
    Mixin crud.
    """

    def __init__(
        self,
        model: Model,
        db_session: Session,
        schema: Type[T],
        query: Optional[FunctionType] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        create_schema: Optional[BaseModel] = None,
        update_schema: Optional[BaseModel] = None,
        error_messages: Optional[Dict] = None,
        has_get_list: bool = True,
        has_update: bool = True,
        has_create: bool = True,
        has_get_one: bool = True,
        has_delete_one: bool = True,
        **kwargs: Any,
    ) -> None:
        self.query = query
        self.error_messages = error_messages

        super().__init__(
            model=model,
            db_session=db_session,
            schema=schema,
            prefix=prefix,
            tags=tags,
            create_schema=create_schema,
            update_schema=update_schema,
            has_get_list=has_get_list,
            has_update=has_update,
            has_create=has_create,
            has_get_one=has_get_one,
            has_delete_one=has_delete_one,
            **kwargs,
        )

    def get_message(self, http_code):
        
        error_mesages = self.error_messages if self.error_messages else {
            "not_found": "Recurso no encontrado.",
            "already_exists": "El dato ya existe.",
        }
        
        return error_mesages.get(http_code)
    
    def _fk_fields(self, model: Model):
        foreign_keys = [c.key for c in model.__table__.c if c.foreign_keys]
        return foreign_keys

    def _get_one_db(self, item_id, query: Query = None):
        item = (
            query.filter(getattr(self.model, self._pk) == item_id).first()
            if self.query
            else self.db_session.query(self.model)
            .filter(getattr(self.model, self._pk) == item_id)
            .first()
        )
        
        msg_response = self.get_message("not_found")

        if not item:
            raise HTTPException(404, msg_response)

        return item

    def _get_paginate(self, *args: Any, **kwargs: Any):
        def route(
            request: Request,
            paginate_params: PaginateParams = Depends(),
        ):

            query = None

            if self.query:
                query = self.query(request)

            path = request.url._url.split("?")[0]
            return self.paginate(
                db_session=self.db_session,
                model=self.model,
                paginate_params=paginate_params,
                squema=self.schema,
                path=path,
                query_model=query,
            )
    

        return route

    def _get_one(self, *args: Any, **kwargs: Any):
        def route(request: Request, item_id):
            query = None
            if self.query:
                query = self.query(request)
            return self._get_one_db(item_id, query)

        return route

    def _create(self, *args: Any, **kwargs: Any):
        def route(model: self.create_schema):

            db_model = self.model(**model.dict())
            self.db_session.add(db_model)
            self.db_session.commit()
            self.db_session.refresh(db_model)

            return db_model

        return route

    def _update(self, *args: Any, **kwargs: Any):
        def route(
            item_id,
            model: self.update_schema,
        ):

            db_model = self._get_one_db(item_id)

            for key, value in model.dict(exclude={self._pk}).items():
                if hasattr(db_model, key):
                    setattr(db_model, key, value)

            self.db_session.commit()
            self.db_session.refresh(db_model)
            return db_model

        return route

    def _delete_one(self, *args: Any, **kwargs: Any):
        def route(request: Request, item_id):
            query = None
            if self.query:
                query = self.query(request)
            db_model = self._get_one_db(item_id, query)
            self.db_session.delete(db_model)
            self.db_session.commit()
            return Response(status_code=204)

        return route
