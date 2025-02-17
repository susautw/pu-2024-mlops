import argparse

from mlops.worker.testing_worker import TestingWorker


def main():
    worker = TestingWorker()



def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Start a worker')
    parser.add_argument('--config', type=str, help='Path to the config file')

    return parser


if __name__ == '__main__':
    main()
