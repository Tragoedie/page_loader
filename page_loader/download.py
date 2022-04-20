"""Download html web page."""
import logging
import os
import pathlib
import shutil
from logging import config
from typing import Any

import requests
from page_loader.get_name import get_folder_name, get_html_name
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
    path_html = os.path.join(directory, get_html_name(url))
    log.info('Downloading from {0} to {1}'.format(url, path_html))
    url_for_download, html = prepare_links(get_response(url).text, url)
    save_html(path_html, html, directory)
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
        try:
            local_file = requests.get(url[0], stream=True)
            local_file.raise_for_status()
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.MissingSchema,
        ) as error:
            log.warning(error)
            raise ExpectedError(
                'Network error when downloading {0}. Status code is {1}'.format(
                    url,
                    requests.get(url).status_code,
                ),
            )
        file_name = os.path.join(files_folder, url[1])
        try:
            with open(file_name, 'wb') as img_file_save:
                for chunk in local_file.iter_content(BYTES_FOR_BLOCK):
                    img_file_save.write(chunk)
        except OSError as err:
            raise ExpectedError(
                'Something gone wrong:{0}, file not saved.'.format(str(err)),
            )
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
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        raise ExpectedError(
            'Network error when downloading {0}. Status code is {1}'.format(
                url,
                requests.get(url).status_code,
            ),
        )


def save_html(path_to_html: str, data_html: Any, path_to_del: str):
    """Save web page.

    Args:
        path_to_html: path to save html
        data_html: text of the web page.
        path_to_del: if need deleted folder.

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    try:
        with open(path_to_html, 'w') as html_file:
            log.info('Save to the {0}'.format(path_to_html))
            html_file.write(data_html)
    except OSError as err:
        shutil.rmtree(path_to_del)
        raise ExpectedError(
            'Something gone wrong:{0}, file not saved.'.format(str(err)),
        )
