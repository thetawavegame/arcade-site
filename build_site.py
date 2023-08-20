#!/usr/bin/env python3
"""Trivial vanilla-python script to copy a file to a directory"""
import enum
import argparse
from pathlib import Path
from typing import Optional, Sequence
import shutil
import sys
import logging

LOGGER = logging.getLogger("metalmancySiteBuilder")


@enum.unique
class AppTier(str, enum.Enum):
    DEV = "dev"
    PROD = "prod"


class CLIArgs(argparse.Namespace):
    tier: AppTier
    verbosity: int


def our_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="build-arcade-site",
        description="Build the arcade.metalmancy.tech website to be served by a CDN/routing thing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "tier",
        help="The application environment. dev or prod.",
        choices=[x.value for x in AppTier.__members__.values()],
        type=AppTier,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbosity of stdout logging",
        action="count",
        default=0,
        dest="verbosity",
    )
    return parser


def run(args: CLIArgs) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if (args.verbosity > 0) else logging.ERROR,
    )
    LOGGER.info(f"Building arcade site with {args=}")
    base_dir = Path(__file__).parent
    config_fname = f"netlify_{args.tier.value}.toml"
    config_file = base_dir / config_fname
    dest_config_path = base_dir / "public" / "netlify.toml"
    if not config_file.exists():  # pragma: no cover
        raise FileNotFoundError(
            f"Make sure that the netlify files exist. {base_dir=} {config_file=}"
        )
    shutil.copy(config_file, dest_config_path)
    LOGGER.info("Copied %s to %s", config_file, dest_config_path)


def main(args: Optional[Sequence[str]] = None):
    parser = our_parser()
    opts: CLIArgs = parser.parse_args(args, CLIArgs())
    run(opts)


if __name__ == "__main__":
    main()
