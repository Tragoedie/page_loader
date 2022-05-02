"""Download html file with local resources."""
import argparse
import logging
import shutil
import sys
from logging import config

from page_loader.download import DEFAULT_PATH, ExpectedError, download
from page_loader.logging import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('page_loader')


def main() -> None:
    """Download html file with local resources."""
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=DEFAULT_PATH,
        help='select folder to download the html page',
    )
    args = parser.parse_args()
    try:
        path = download(args.url, args.output)
    except ExpectedError as error:
        shutil.rmtree(args.output)
        log.error(error)
        sys.exit(1)
    print(path)
    sys.exit(0)


if __name__ == '__main__':
    main()
