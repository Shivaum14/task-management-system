from typing import Any, Dict, OrderedDict, Type

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property


class RestMixin:
    """Mixin class to provide serialization utilities for SQLAlchemy models."""

    def dict(self, relations: bool = False, private: bool = False) -> Dict[str, Any]:
        """
        Convert the SQLAlchemy model instance into a dictionary.

        Args:
            relations (bool): If True, include to-one relationships using their `dict()` methods.
                              To prevent deep recursion, nested calls set `relations=False`.
            private (bool): If True, include fields marked with `private=True`.

        Returns:
            Dict[str, Any]: Serialized dictionary of the model.
        """
        inspected_model = inspect(self.__class__)

        d = OrderedDict()

        for col in inspected_model.column_attrs:
            if len(col.columns) == 0:
                continue
            if not private and getattr(col.columns[0], "private", False):
                continue
            d[col.key] = getattr(self, col.key)

        for composite in inspected_model.composites:
            raise NotImplementedError()

        for key, item in inspected_model.all_orm_descriptors.items():
            if not isinstance(item, hybrid_property):
                continue
            if private or not getattr(item, "private", False):
                d[key] = getattr(self, key)

        for relation in inspected_model.relationships:
            if (private or not getattr(relation, "private", False)) and relations:
                r = getattr(self, relation.key)
                if hasattr(r, "dict"):
                    d[relation.key] = r.dict(private=private, relations=False)  # prevent deep relations

        return d

    def to_schema(self, schema_cls: Type) -> Any:
        """
        Convert the model instance to a Pydantic schema object.

        Args:
            schema_cls (Type): Pydantic model class to instantiate.

        Returns:
            Any: Instance of the given Pydantic model.
        """
        return schema_cls(**self.dict())
