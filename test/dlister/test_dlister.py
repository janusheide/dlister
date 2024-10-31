# Copyright (c) 2024, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import sys

import pytest
from packaging.requirements import Requirement

from dlister.dlister import cli, list_requirement, main


def test_list_requirement():
    assert list_requirement(Requirement("hejsa>=2.0.1"), match_operators=[">="], skip=[]) == Requirement("hejsa==2.0.1")
    assert list_requirement(Requirement("hejsa>=2.0.0"), match_operators=[">="], skip=["hejsa"]) is None

def test_list_requirements():
    pass


def test_cli():

    with pytest.raises(SystemExit):
        assert cli(["--help"])

    with pytest.raises(SystemExit):
        assert cli(["--version"])

    a = vars(cli(["--log-level", "INFO"]))
    assert a["log_file"] is None
    assert a["log_level"] == "INFO"

    a = vars(cli(["--skip", "foo", "bar"]))
    assert a["skip"] == ["foo", "bar"]


def test_main(tmp_path):
    arguments = vars(cli(sys.argv[1:]))
    main(**arguments)

    d = tmp_path / "foo"
    d.mkdir()
    p = d / "bar"
    p.write_text("[foobar]")

    arguments["infile"] = p.open("rb")
    with pytest.raises(SystemExit):
        main(**arguments)

    p.write_text("kazhing")
    arguments["infile"] = p.open("rb")
    with pytest.raises(SystemExit):
        main(**arguments)
