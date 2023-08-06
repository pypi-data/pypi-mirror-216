from inspect import isclass
from typing import TYPE_CHECKING, Any, Dict, Type, cast

from pydantic import BaseConfig, BaseModel, create_model
from pyfactories.utils import create_model_from_dataclass

if TYPE_CHECKING:
    from pydantic.fields import ModelField


class Config(BaseConfig):
    arbitrary_types_allowed = True


def create_parsed_model_field(value: Type[Any]) -> "ModelField":
    """Create a pydantic model with the passed in value as its sole field, and
    return the parsed field."""
    model = create_model("temp", __config__=Config, **{"value": (value, ... if not repr(value).startswith("typing.Optional") else None)})  # type: ignore
    return cast("BaseModel", model).__fields__["value"]


_dataclass_model_map: Dict[Any, Type[BaseModel]] = {}


def convert_dataclass_to_model(dataclass: Any) -> Type[BaseModel]:
    """Converts a dataclass to a pydantic model and memoizes the result."""
    if not isclass(dataclass) and hasattr(dataclass, "__class__"):
        dataclass = dataclass.__class__
    if not _dataclass_model_map.get(dataclass):
        _dataclass_model_map[dataclass] = create_model_from_dataclass(dataclass)  # pyright: ignore
    return _dataclass_model_map[dataclass]
