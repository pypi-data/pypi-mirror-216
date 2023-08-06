from pydantic import BaseModel, Extra, Field
from typing import Literal


class Load(BaseModel, extra=Extra.forbid):
    path: str
    intoObject: str
    asType: Literal["datagram", "table", "netcdf"] = "netcdf"
