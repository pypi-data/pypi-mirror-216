from pydantic import BaseModel, Field, Extra
from typing import Sequence, Any, Dict


class Transpose(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    table: str
    using: Any
    into: str
