from pydantic import BaseModel, Extra, Field
from typing import Literal


class Save(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    """Save a table into an external (``pkl``, ``xlsx``) file."""

    table: str
    """The name of the table loaded in memory to be stored."""

    as_: str = Field(alias="as")
    """Path to which the table is stored."""

    type: Literal["pkl", "json", "xlsx", "csv"] = None
    """
    Type of the output file.

    .. note::

        Round-tripping of **dgpost** data is only possible using the ``pkl`` format. The
        ``json`` format may however be better suited for long-term storage. The other
        formats (``xlsx`` and ``csv``) are provided for convenience only and should not
        be used for chaining of **dgpost** runs.
    """

    sigma: bool = True
    """Whether uncertainties/error estimates in the data should be stripped. Particularly
    useful when exporting into ``xlsx`` or ``csv``."""
