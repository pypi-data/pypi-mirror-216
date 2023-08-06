"""
The CLI entrypoints and config parsers.
"""
from argparse import ArgumentParser
from configparser import ConfigParser
import pathlib

from . import __version__
from .program_request import ProgramRequest


def parse_args(args):
    parser = ArgumentParser(
        description="A tool to download OBs from the ESO archive",
    )

    parser.add_argument(
        '--version', action='version', version='%(prog)s ' + __version__
    )

    parser.add_argument(
        "--config", action="store", type=pathlib.Path,
    )

    parser.add_argument(
        "program_ids", nargs="+"
    )

    return parser.parse_args(args)


def parse_config(path):
    if path is not None:
        conf = ConfigParser()
        with path.open() as file:
            conf.read_file(file)
        return Config(conf)
    raise ConfigError("No config file provided")


class ConfigError(Exception):
    pass


class Config:  # pylint: disable=too-few-public-methods
    def __init__(self, cfg):
        self._cfg = cfg
        self._programs = set(cfg.sections())
        defaults = cfg.defaults()
        try:
            self._default_username = defaults["username"]
        except KeyError:
            raise ConfigError("Set a default username")
        try:
            self._default_base_dir = defaults["base_dir"]
        except KeyError:
            raise ConfigError("Set a default base_dir")

    def program_requests_from_program_ids(self, program_ids):
        for id_ in program_ids:
            yield ProgramRequest(
                program_id=id_,
                username=self._cfg.get(
                    id_, "username", fallback=self._default_username
                ),
                base_dir=self._cfg.get(
                    id_, "base_dir", fallback=self._default_base_dir
                ),
            )


def main(args=None):
    parsed_args = parse_args(args)

    try:
        config = parse_config(parsed_args.config)
    except ConfigError as exc:
        print(f"Failed to parse config: {exc}")
        return 1

    for program_request in config.program_requests_from_program_ids(
        parsed_args.program_ids
    ):
        program_request.log_start()
        program_request.download_files()
        program_request.log_end()
    return 0
