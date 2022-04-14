"""Download html web page."""
import logging
import os
from logging import config

import requests
from page_loader.get_name import get_folder_name, get_html_name
from page_loader.html_parser import IMG, replace_links
from page_loader.logging_settings import LOGGING_CONFIG
from progress.bar import ChargingBar

config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('page_loader')


BYTES_FOR_BLOCK = 4096


class ExpectedError(Exception):
    """Class for errors expected of program."""

    pass


def download(url: str, directory: str) -> str:
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
    files_folder = os.path.join(directory, get_folder_name(url))
    try:
        log.info('Create folder: {0}'.format(files_folder))
        os.makedirs(files_folder, exist_ok=True)
    except PermissionError:
        raise ExpectedError(
            'You have not access to directory: {0}'.format(
                directory,
            ),
        )
    except FileNotFoundError:
        raise ExpectedError(
            'Choose a valid directory path, please: {0}'.format(
                directory,
            ),
        )
    except OSError as error:
        raise ExpectedError('Unknown {0} error'.format(str(error)))
    download_path = download_html(url, directory)
    log.info('Downloading from {0} to {1}'.format(url, download_path))
    url_for_download = replace_links(download_path, url)
    download_local_files(url_for_download, directory)
    log.info('Done!')
    return download_path


def download_html(url: str, directory: str) -> str:
    """Download html web page.

    Args:
        url: url of the web page.
        directory: directory where to download html page.

    Returns:
        Full path of download with file_name.

    Raises:
        ExpectedError: permission or not found errors in file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise ExpectedError(
            'Network error when downloading {0}. Status code is {1}'.format(
                url,
                requests.get(url).status_code,
            ),
        )
    file_name = get_html_name(url)
    download_path_name = os.path.join(directory, file_name)
    try:
        with open(download_path_name, 'w') as html_file:
            html_file.write(response.text)
    except OSError as err:
        raise ExpectedError(
            'Something gone wrong:{0}, file not saved.'.format(str(err)),
        )
    return download_path_name


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
        file_folder = os.path.join(files_folder, url[1])
        try:
            if url[2] is IMG:
                with open(file_folder, 'wb') as img_file_save:
                    for chunk in local_file.iter_content(BYTES_FOR_BLOCK):
                        img_file_save.write(chunk)
            else:
                with open(file_folder, 'w') as other_file_save:
                    other_file_save.write(local_file.text)
        except OSError as err:
            raise ExpectedError(
                'Something gone wrong:{0}, file not saved.'.format(str(err)),
            )
        charging_bar.next()
    charging_bar.finish()
