"""Download html file with local resources."""
import argparse
import os

from page_loader.download_function import download


def main() -> None:
    """Download html file with local resources."""
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=os.getcwd(),
        help='select folder to download the html page',
    )
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
