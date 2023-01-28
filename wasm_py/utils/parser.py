from argparse import ArgumentParser
from argparse import Namespace


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--wasm",
        required=True,
        help="Path to .wasm",
        type=str,
    )
    return parser.parse_args()
