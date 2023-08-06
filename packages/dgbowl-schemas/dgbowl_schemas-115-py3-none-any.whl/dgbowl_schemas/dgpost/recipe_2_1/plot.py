from pydantic import BaseModel, Extra, Field
from typing import Literal, Sequence, Optional, Tuple, Any, Dict


class SeriesIndex(BaseModel, extra=Extra.forbid):
    from_zero: bool = True
    to_units: Optional[str]


class Series(BaseModel, extra=Extra.allow):
    y: str
    x: Optional[str]
    kind: Literal["scatter", "line", "errorbar"] = "scatter"
    index: Optional[SeriesIndex] = SeriesIndex()


class AxArgs(BaseModel, extra=Extra.allow):
    cols: Optional[Tuple[int, int]]
    rows: Optional[Tuple[int, int]]
    series: Sequence[Series]
    methods: Optional[Dict[str, Any]]
    legend: bool = False


class PlotSave(BaseModel, extra=Extra.allow, allow_population_by_field_name=True):
    as_: str = Field(alias="as")
    tight_layout: Optional[Dict[str, Any]]


class Plot(BaseModel, extra=Extra.forbid):
    """Plot data from a single table."""

    table: str
    """The name of the table loaded in memory to be plotted."""

    nrows: int = 1
    """Number of rows in the figure grid."""

    ncols: int = 1
    """Number of columns in the figure grid."""

    fig_args: Optional[Dict[str, Any]]
    """Any optional method calls for the figure; passed to ``matplotlib``."""

    ax_args: Sequence[AxArgs]
    """Specifications of the figure axes, including selection of data for the plots."""

    style: Optional[Dict[str, Any]]
    """Specification of overall ``matplotlib`` style."""

    save: Optional[PlotSave]
    """Arguments for saving the plotted figure into files."""
