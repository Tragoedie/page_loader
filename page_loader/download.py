"""Download html web page."""
import logging
import os
import pathlib

from logging import config
from typing import Any

import requests
from page_loader.names import get_folder_name, get_html_name
from page_loader.html import prepare_links
from page_loader.logging import LOGGING_CONFIG
from progress.bar import ChargingBar

config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('page_loader')

BYTES_FOR_BLOCK = 1024
DEFAULT_PATH = os.getcwd()


class ExpectedError(Exception):
    """Class for errors expected of program."""

    pass


def download(url: str, directory: str = DEFAULT_PATH) -> str:
    """Download html web page and files on it.

    Args:
        url: url of the web page.
        directory: directory where download html page.

    Returns:
        Full path of download with file_name

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    log.info('Start downloading!')
    path_local_folder = os.path.join(directory, get_folder_name(url))
    path_html = os.path.join(directory, get_html_name(url))
    log.info('Downloading from {0} to {1}'.format(url, path_html))
    url_for_download, html = prepare_links(
        get_response(url).text,
        url,
    )
    try:
        log.info('Create folder: {0}'.format(path_local_folder))
        pathlib.Path(path_local_folder).mkdir(exist_ok=True)
    except FileNotFoundError:
        raise ExpectedError(
            'Choose a valid directory path, please: {0}'.format(
                directory,
            ),
        )
    except PermissionError:
        raise ExpectedError(
            'You have not access to directory: {0}'.format(
                directory,
            ),
        )
    except OSError as error:
        raise ExpectedError('Unknown {0} error'.format(str(error)))
    save_data(path_html, html)
    download_local_files(url_for_download, directory)
    log.info('Done!')
    return path_html


def download_local_files(urls, files_folder) -> None:
    """Download html web page.

    Args:
        urls: array of links to download files.
        files_folder: directory where to download local files.

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    charging_bar = ChargingBar('Loading...', max=len(urls))
    log.info('Saving to the {0}'.format(files_folder))
    log.info('Download resources...')
    for url in urls:
        local_file = get_response(url[0])
        file_name = os.path.join(files_folder, url[1])
        save_data(file_name, local_file)
        charging_bar.next()
    charging_bar.finish()


def get_response(url: str) -> Any:
    """Download data of web page.

    Args:
        url: url of the web page.

    Returns:
        response html file.

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        raise ExpectedError(
            'Network error when downloading {0}. Status code is {1}'.format(
                url,
                requests.get(url).status_code,
            ),
        )


def save_data(path_to_html: str, data: Any) -> None:
    """Save web page.

    Args:
        path_to_html: path to save html
        data: resources of web page.

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    try:
        with open(path_to_html, 'wb') as data_file:
            log.info('Save to the {0}'.format(path_to_html))
            data_file.write(data)
    except OSError as err:
        raise ExpectedError(
            'Something gone wrong:{0}, file not saved.'.format(str(err)),
        )
