from pydantic import BaseModel, Extra, validator
from typing import Optional, Tuple, Union
import locale
import tzlocal


class StepDefaults(BaseModel, extra=Extra.forbid):
    """Configuration of defaults applicable for all steps."""

    timezone: str = "localtime"
    """Global timezone specification.

    .. note::

        This should be set to the timezone where the measurements have been
        performed, as opposed to the timezone where ``yadg`` is being executed.
        Otherwise timezone offsets may not be accounted for correctly.

    """

    locale: Union[Tuple[str, str], str] = None
    """Global locale specification. Will default to current locale."""

    encoding: Optional[str] = None
    """Global filetype encoding. Will default to ``None``."""

    @validator("timezone", always=True)
    @classmethod
    def timezone_resolve_localtime(cls, v):
        if v == "localtime":
            v = tzlocal.get_localzone_name()
        return v

    @validator("locale", always=True)
    @classmethod
    def locale_set_default(cls, v):
        if v is None:
            v = ".".join(locale.getlocale())
        return v
