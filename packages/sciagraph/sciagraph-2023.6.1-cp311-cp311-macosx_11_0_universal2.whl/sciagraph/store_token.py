"""Store an access token on disk."""

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from importlib.util import find_spec

from ._initialization import _load_module

PARSER = ArgumentParser(
    usage="python -m sciagraph.store_token ACCESS_KEY ACCESS_SECRET",
    epilog="To get the correct access token, "
    + "visit https://account.sciagraph.com/ui/ and [Copy] the command-line.\n\n"
    + "*** Need help? Have questions? Email support@sciagraph.com ***",
    formatter_class=RawDescriptionHelpFormatter,
    allow_abbrev=False,
)
PARSER.add_argument("access_key")
PARSER.add_argument("access_secret")
PARSER.add_argument("metadata", nargs="?", default=None)


def main():
    argv = sys.argv[1:]

    if len(argv) < 2:
        PARSER.print_help()
        sys.exit(0)

    args = PARSER.parse_args(argv)
    setup = _load_module("_sciagraph_setup", find_spec("sciagraph._sciagraph").origin)
    try:
        path = setup.store_api_token(args.access_key, args.access_secret, args.metadata)
    except RuntimeError as e:
        print(
            f"Error: {e}\n\nTo get the correct access token, "
            + "visit https://account.sciagraph.com/ui/ and [Copy] the command-line.",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        print(
            f"Stored the access token in {path}\n\nYou can now profile code with "
            + "Sciagraph, for example 'python -m sciagraph run yourcode.py'."
        )


if __name__ == "__main__":
    main()
