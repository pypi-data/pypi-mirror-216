from pydantic import BaseModel, Extra, Field
from typing import Sequence
from .metadata import Metadata
from .step import Steps
from .stepdefaults import StepDefaults
from .filetype import ExtractorFactory, FileType


class DataSchema(BaseModel, extra=Extra.forbid):
    """
    :class:`DataSchema` introduced in ``yadg-5.0``.
    """

    metadata: Metadata
    """Input metadata for ``yadg``."""

    step_defaults: StepDefaults = Field(StepDefaults())
    """Default values for configuration of ``yadg``'s parsers."""

    steps: Sequence[Steps]
    """Input commands for ``yadg``'s parsers, organised as a sequence of steps."""


__all__ = ["DataSchema", "Metadata", "FileType", "ExtractorFactory"]
