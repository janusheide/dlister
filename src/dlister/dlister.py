# Copyright (c) 2024, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.

"""Print or save to a file project dependencies from pyproject.toml."""

from __future__ import annotations

import sys
from argparse import (
    ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace,
)
from importlib.metadata import version
from logging import basicConfig, getLevelName, getLogger
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsRead

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

try:
    from tomllib import TOMLDecodeError, load  # type: ignore
except ModuleNotFoundError:
    from tomli import TOMLDecodeError, load  # type: ignore

logger = getLogger(__name__)


def list_requirement(
    requirement: Requirement,
    *,
    skip: list[str],
    match_operators: list[str],
) -> Requirement | None:
    """Find requirement."""
    if requirement.name in skip:
        return None

    for s in requirement.specifier:
        if s.operator in match_operators:
            requirement.specifier = SpecifierSet(f"=={s.version}")
            return requirement

    return None


def list_requirements(
    dependencies: list[str],
    **kwargs
) -> list[str]:
    """Find requirements."""
    return [str(r) for r in [list_requirement(Requirement(d), **kwargs) for d in dependencies] if r]


def main(
    *,
    log_file: Path,
    log_level: str,
    infile: SupportsRead[bytes],
    dependencies: list[str],
    output,
    **kwargs,
) -> None:
    """Main."""
    basicConfig(
        filename=log_file,
        level=getLevelName(log_level),
        format = "%(levelname)s: %(message)s",
    )
    try:
        data = load(infile)
    except TOMLDecodeError:
        logger.critical(f"Error parsing input toml file: {infile}")
        exit(1)

    project = data.get("project")
    if project is None:
        logger.critical(f"No project section in input file: {infile}")
        exit(1)

    [output.write(f"{r}\n") for r in list_requirements(project.get("dependencies", []), **kwargs)]

    for k,v in project.get("optional-dependencies").items():
        [output.write(f"{r}\n") for r in list_requirements(v, **kwargs)
            if k in dependencies or "*" in dependencies]


def cli(args) -> Namespace:
    """Parse arguments."""
    parser = ArgumentParser(
        description="Print Python Project Dependencies.",
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "dependencies", type=str, nargs="*", default=[],
        help="optional dependencies to include, use '*' to match all",
        )

    parser.add_argument(
        "-i", "--infile",
        default="pyproject.toml",
        type=FileType("rb"),
        help="path(s) to input file(s)",
        )

    parser.add_argument(
        "-o", "--output",
        default=sys.stdout,
        type=FileType("w"),
        help="output file.",
        )

    parser.add_argument(
        "-m", "--match-operators", nargs="*",
        default=["==", ">="],
        choices=["<", "<=", "==", ">=", ">", "~="],
        help="operators to print.")

    parser.add_argument(
        "--skip", type=str, nargs="*", default=[],
        help="dependencies to skip.")

    parser.add_argument(
        "--log-level", default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="logging level.")

    parser.add_argument(
        "--log-file",
        type=Path,
        help="pipe loggining to file instead of stdout.")

    parser.add_argument("-v", "--version", action="version", version=version("dlister"))

    return parser.parse_args(args)


def main_cli() -> None:
    """Main."""
    main(**vars(cli(sys.argv[1:])))


if __name__ == "__main__":
    main_cli()
