import argparse
from typing import NamedTuple


def main():
    pass


class Args(NamedTuple):
    host: str
    port: int


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start the MLOps cluster")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="The host to bind to")
    parser.add_argument("--port", type=int, default=19000, help="The port to bind to")
    return parser


if __name__ == "__main__":
    main()
