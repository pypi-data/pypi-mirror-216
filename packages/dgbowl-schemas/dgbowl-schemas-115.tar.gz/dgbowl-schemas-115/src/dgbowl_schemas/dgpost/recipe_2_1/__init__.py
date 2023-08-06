from pydantic import BaseModel, Extra
from typing import Optional, Literal, Sequence
from .load import Load
from .extract import Extract
from .pivot import Pivot
from .transform import Transform
from .plot import Plot
from .save import Save


class Recipe(BaseModel, extra=Extra.forbid):
    """
    A Pydantic Class implementing version 2.1 of the **Recipe** model for **dgpost**.
    """

    version: Literal["2.1"]

    load: Optional[Sequence[Load]]
    """Select external files (``NetCDF`` or ``json`` datagrams, ``pkl`` tables) to load."""

    extract: Optional[Sequence[Extract]]
    """Extract columns from loaded files into tables, interpolate as necessary."""

    pivot: Optional[Sequence[Pivot]]
    """Reorder tables by grouping rows into arrays using columns as indices."""

    transform: Optional[Sequence[Transform]]
    """Calculate and otherwise transform the data in the tables."""

    plot: Optional[Sequence[Plot]]
    """Plot data from a single table."""

    save: Optional[Sequence[Save]]
    """Save a table into an external (``pkl``, ``xlsx``) file."""
