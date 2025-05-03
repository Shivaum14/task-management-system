from typing import Any

from sqlalchemy.orm import MappedColumn
from sqlalchemy.orm import mapped_column as default_mapped_column


def mapped_column(*args: Any, private: bool = False, **kwargs: Any) -> MappedColumn[Any]:
    info = kwargs.pop("info", {})
    info["private"] = private
    return default_mapped_column(*args, info=info, **kwargs)
