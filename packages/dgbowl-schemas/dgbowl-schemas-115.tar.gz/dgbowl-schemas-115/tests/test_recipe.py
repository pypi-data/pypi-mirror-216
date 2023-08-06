import pytest
import os
import yaml
import json
from dgbowl_schemas import to_recipe

from ref_recipe import ts0, ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9
from ref_recipe import js0
from ref_recipe import pivot1, pivot2


@pytest.mark.parametrize(
    "inpath, outdict",
    [
        ("le_1.yaml", ts0),
        ("le_2.yaml", ts1),
        ("lee_1.yaml", ts2),
        ("lee_2.yaml", ts3),
        ("les_1.yaml", ts4),
        ("les_2.yaml", ts5),
        ("let_1.yaml", ts6),
        ("let_2.yaml", ts7),
        ("letp_1.yaml", ts8),
        ("lp_1.yaml", ts9),
        ("pivot_1.yaml", pivot1),
        ("pivot_2.yaml", pivot2),
    ],
)
def test_recipe_from_yml(inpath, outdict, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        indict = yaml.safe_load(infile)
    ret = to_recipe(**indict).dict(by_alias=True)
    assert outdict == ret


@pytest.mark.parametrize(
    "inpath, outdict",
    [("lets.json", js0)],
)
def test_recipe_from_json(inpath, outdict, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        indict = json.load(infile)
    ret = to_recipe(**indict).dict(by_alias=True)
    assert outdict == ret


@pytest.mark.parametrize(
    "inpath",
    [
        ("le_1.yaml"),  # 1.0
        ("letp_1.yaml"),  # 1.0
    ],
)
def test_recipe_update_chain(inpath, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = yaml.safe_load(infile)
    ret = to_recipe(**jsdata)
    while hasattr(ret, "update"):
        print("here")
        ret = ret.update()
    assert ret.version == "2.1"
