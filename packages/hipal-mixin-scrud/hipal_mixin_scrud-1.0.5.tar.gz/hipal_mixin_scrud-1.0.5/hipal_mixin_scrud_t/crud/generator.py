# lib
from typing import Any, Callable, List, Optional, Sequence, TypeVar, Union
from abc import ABC, abstractmethod
from pydantic import create_model
from pydantic import BaseModel
from typing import Generic
from typing import Type

# fastapi
from fastapi import APIRouter, Depends, HTTPException

# sqlalchemy
from sqlalchemy.orm import Session

# app
from schemas.pagination_base import PaginationBase

T = TypeVar("T", bound=BaseModel)

DEPENDENCIES = Optional[Sequence[Depends]]


class MixinGenerator(Generic[T], APIRouter, ABC):
    """
    Mixin crud.
    """

    _base_path: str = "/"

    def schema_factory(
        self, schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
    ) -> Type[T]:
        """
        Is used to create a CreateSchema which does not contain pk
        """

        exclude_fields = [
            "created_at",
            "updated_at",
            pk_field_name,
        ]

        fields = {
            f.name: (f.type_, ...)
            for f in schema_cls.__fields__.values()
            if f.name not in exclude_fields
        }

        name = schema_cls.__name__ + name
        schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
        return schema

    def __init__(
        self,
        model,
        db_session: Session,
        schema: Type[T],
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        create_schema: Optional[BaseModel] = None,
        update_schema: Optional[BaseModel] = None,
        has_get_list: bool = True,
        has_update: bool = True,
        has_create: bool = True,
        has_get_one: bool = True,
        has_delete_one: bool = True,
        **kwargs: Any,
    ) -> None:
        self.model = model
        self.db_session = db_session
        self.schema = schema
        self._pk: str = self._pk if hasattr(self, "_pk") else "id"
        self.create_schema = (
            create_schema
            if create_schema
            else self.schema_factory(self.schema, pk_field_name=self._pk, name="Create")
        )
        self.update_schema = (
            update_schema
            if update_schema
            else self.schema_factory(self.schema, pk_field_name=self._pk, name="Update")
        )

        prefix = str(prefix if prefix else self.schema.__name__).lower()
        prefix = self._base_path + prefix.strip("/")
        tags = tags or [prefix.strip("/").capitalize()]
        super().__init__(prefix=prefix, tags=tags, **kwargs)

        if has_get_list:
            self._add_api_route(
                "",
                self._get_paginate(),
                methods=["GET"],
                response_model=PaginationBase,  # type: ignore
                summary="Paginate data",
                dependencies=[],
            )

        if has_create:
            self._add_api_route(
                "",
                self._create(),
                methods=["POST"],
                response_model=self.schema,
                summary="Create One",
                dependencies=[],
            )

        if has_get_one:
            self._add_api_route(
                "/{item_id}",
                self._get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
                dependencies=[],
            )

        if has_update:
            self._add_api_route(
                "/{item_id}",
                self._update(),
                methods=["PUT"],
                response_model=self.schema,
                summary="Update One",
                dependencies=[],
            )

        if has_delete_one:
            self._add_api_route(
                "/{item_id}",
                self._delete_one(),
                methods=["DELETE"],
                summary="Delete One",
                dependencies=[],
            )

    def _add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        dependencies: Union[bool, DEPENDENCIES],
        error_responses: Optional[List[HTTPException]] = None,
        **kwargs: Any,
    ) -> None:
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        super().add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, **kwargs
        )

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                route.path == f"{self.prefix}{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    @abstractmethod
    def _get_paginate(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError
