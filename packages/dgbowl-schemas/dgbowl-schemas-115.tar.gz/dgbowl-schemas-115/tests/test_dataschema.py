import pytest
import os
import json
from dgbowl_schemas import to_dataschema
from dgbowl_schemas.yadg import ExtractorFactory
import locale


@pytest.mark.parametrize(
    "inpath, success",
    [
        ("metadata_ts0.json", True),
        ("metadata_ts1.json", False),
        ("metadata_ts2.json", True),
        ("metadata_ts3.json", False),
        ("metadata_ts4.json", False),
        ("metadata_ts5.json", True),
        ("metadata_ts6.json", False),
        ("metadata_ts7.json", False),
        ("metadata_ts8.json", True),
        ("metadata_ts9.json", True),
        ("metadata_ts10.json", True),
    ],
)
def test_dataschema_metadata_json(inpath, success, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        indict = json.load(infile)
    if not success:
        with pytest.raises(ValueError):
            to_dataschema(**indict)
    else:
        to_dataschema(**indict)


@pytest.mark.parametrize(
    "inpath",
    [
        ("ts0_dummy.json"),  # 4.0
        ("ts1_dummy.json"),  # 4.0.1
        ("ts2_dummy.json"),  # 4.1
        ("ts3_basiccsv.json"),  # 4.0.1
        ("ts4_basiccsv.json"),  # 4.1
        ("ts5_flowdata.json"),  # 4.0.1
        ("ts6_meascsv.json"),  # 4.1
        ("ts7_electrochem.json"),  # 4.1
        ("ts8_chromdata.json"),  # 4.2
        ("ts9_basiccsv.json"),  # 4.2
        ("ts10_chromdata.json"),  # 5.0
        ("ts11_basiccsv.json"),  # 5.0
        ("ts12_dummy.json"),  # 5.0
    ],
)
def test_dataschema_steps_json(inpath, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = json.load(infile)
    ref = jsdata["output"]
    ret = to_dataschema(**jsdata["input"])
    assert ret.dict()["steps"] == ref


@pytest.mark.parametrize(
    "inpath",
    [
        ("err0_chromtrace.json"),  # 4.1
        ("err1_typo.json"),  # 4.1
        ("err2_chromdata.json"),  # 4.2
        ("err3_typo.json"),  # 4.2
        ("err4_chromdata.json"),  # 5.0
        ("err5_typo.json"),  # 5.0
        ("err6_chromtrace.json"),  # 4.0
        ("err7_typo.json"),  # 4.0
        ("err8_metadata.json"),  # 5.0
    ],
)
def test_dataschema_err(inpath, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = json.load(infile)
    with pytest.raises(ValueError) as e:
        to_dataschema(**jsdata["input"])
    assert jsdata["exception"] in str(e.value)


@pytest.mark.parametrize(
    "inpath",
    [
        ("up0_chromtrace.json"),  # 4.0
        ("up1_chromtrace.json"),  # 4.1
        ("up2_chromtrace.json"),  # 4.2
        ("up3_chromdata.json"),  # 4.2
    ],
)
def test_dataschema_update(inpath, datadir):
    locale.setlocale(locale.LC_CTYPE, "en_GB.UTF-8")
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = json.load(infile)
    ref = jsdata["output"]
    ret = to_dataschema(**jsdata["input"]).update()
    print(ret)
    assert ref == ret.dict(exclude_none=True)


@pytest.mark.parametrize(
    "inpath",
    [
        ("chain_vna_4.0.json"),  # 4.0
        ("chain_gc_4.0.json"),  # 4.0
        ("chain_basiccsv_4.1.json"),  # 4.1
    ],
)
def test_dataschema_update_chain(inpath, datadir):
    locale.setlocale(locale.LC_CTYPE, "en_GB.UTF-8")
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = json.load(infile)
    ret = to_dataschema(**jsdata)
    while hasattr(ret, "update"):
        ret = ret.update()
    assert ret.metadata.version == "5.0"


@pytest.mark.parametrize(
    "input, output",
    [
        (  # ts0 - mpr file, fill in global defaults
            {
                "filetype": "eclab.mpr",
            },
            {
                "filetype": "eclab.mpr",
                "locale": "en_GB.UTF-8",
            },
        ),
        (  # ts1 - mpt file, mixture of inputs and defaults from extractor
            {
                "filetype": "eclab.mpt",
                "locale": "de_DE.UTF-8",
                "timezone": "Europe/Zurich",
            },
            {
                "filetype": "eclab.mpt",
                "locale": "de_DE.UTF-8",
                "timezone": "Europe/Zurich",
                "encoding": "windows-1252",
            },
        ),
    ],
)
def test_extractor_factory(input, output):
    locale.setlocale(locale.LC_CTYPE, "en_GB.UTF-8")
    ret = ExtractorFactory(extractor=input).extractor
    assert ret.filetype == output.get("filetype")
    assert ret.locale == output.get("locale")
    assert ret.encoding == output.get("encoding")
    assert ret.timezone is not None
