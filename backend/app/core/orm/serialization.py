"""Mixin class to provide serialization utilities for SQLAlchemy models."""

import json
from collections import OrderedDict
from typing import Any, Generator, Type

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property


class SerializableMixin:
    """Mixin class to provide serialization utilities for SQLAlchemy models."""

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        """Allow unpacking or conversion using `dict(model_instance)`."""
        for name in self.get_properties():
            yield name, getattr(self, name)

    def dict(
        self,
        relations: bool = False,
        private: bool = False,
    ) -> "OrderedDict[str, Any]":
        """Serialize the model to an ordered dictionary."""
        return OrderedDict(
            (name, getattr(self, name))
            for name in self.get_properties(
                private=private,
                relations=relations,
            )
        )

    def json(
        self,
        relations: bool = False,
        private: bool = False,
    ) -> str:
        """Serialize the model to a JSON string."""
        return json.dumps(
            self.dict(
                private=private,
                relations=relations,
            ),
            default=str,
        )

    def to_schema(self, schema_cls: Type[BaseModel]) -> Any:
        """
        Convert the model instance to a Pydantic schema object.

        Args:
            schema_cls (Type): Pydantic model class to instantiate.

        Returns:
            Any: Instance of the given Pydantic model.
        """
        return schema_cls(**self.dict())

    def get_properties(
        self,
        private: bool = False,
        relations: bool = False,
    ) -> Generator[str, None, None]:
        """Yield the names of serializable properties.

        This includes columns, hybrid properties, and optionally relationships.
        Respects `info={"private": True}` if `private=False`.

        Args:
            private (bool): Whether to include private fields.
            relations (bool): Whether to include relationship properties.

        Yields:
            str: Attribute name.
        """
        model_cls: Type["SerializableMixin"] = type(self)
        mapper = inspect(model_cls)
        assert mapper is not None

        # Regular column attributes
        for attr in mapper.column_attrs:
            col = attr.columns[0] if attr.columns else None
            if col is not None and (private or not getattr(col, "info", {}).get("private", False)):
                yield attr.key

        # Hybrid properties
        for key, attr in vars(model_cls).items():
            if isinstance(attr, hybrid_property):
                if private or not getattr(attr, "private", False):
                    yield key

        # Relationships (optional)
        if relations:
            for rel in mapper.relationships:
                if private or not getattr(rel, "info", {}).get("private", False):
                    yield rel.key
