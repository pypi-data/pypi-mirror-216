import argparse
from pathlib import Path
import sys

from tableau_helpers import server


def _parse_args(args) -> argparse.Namespace:
    description = "Upload or overwrite a hyperfile on tableau-server"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--hyperfile",
        type=Path,
        required=True,
        help="The path to the hyperfile to be uploaded.",
    )
    parser.add_argument(
        "--dest",
        type=str,
        required=True,
        help="The destination project string from root folder",
    )
    parser.add_argument(
        "--new-name",
        type=str,
        required=False,
        default=None,
        help="A name for the datasource (if desired different from hyperfile)",
    )
    return parser.parse_args(args)


def main(args):
    args = _parse_args(args)
    server.create_or_replace_hyper_file(
        project=args.dest, hyperfile_path=args.hyperfile, name=args.new_name
    )


def entry_point():
    main(sys.argv[1:])


if __name__ == "__main__":
    entry_point()
