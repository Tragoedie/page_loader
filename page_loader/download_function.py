"""Download html web page."""
import os

import requests
from page_loader.get_name import get_folder_name, get_html_name
from page_loader.html_parser import IMG, replace_links
from progress.bar import ChargingBar

BYTES_FOR_BLOCK = 4096


def download(url: str, directory: str) -> str:
    """Download html web page and files on it.

    Args:
        url: url of the web page.
        directory: directory where download html page.

    Returns:
        Full path of download with file_name
    """
    files_folder = os.path.join(directory, get_folder_name(url))
    os.makedirs(files_folder, exist_ok=True)
    download_path = download_html(url, directory)
    url_for_download = replace_links(download_path, url)
    download_local_files(url_for_download, directory)
    return download_path


def download_html(url: str, directory: str) -> str:
    """Download html web page.

    Args:
        url: url of the web page.
        directory: directory where to download html page.

    Returns:
        Full path of download with file_name
    """
    response = requests.get(url).text
    file_name = get_html_name(url)
    download_path_name = os.path.join(directory, file_name)
    with open(download_path_name, 'w') as html_file:
        html_file.write(response)
    return download_path_name


def download_local_files(urls, files_folder) -> None:
    """Download html web page.

    Args:
        urls: array of links to download files.
        files_folder: directory where to download local files.
    """
    charging_bar = ChargingBar('Loading...', max=len(urls))
    for url in urls:
        local_file = requests.get(url[0], stream=True)
        file_folder = os.path.join(files_folder, url[1])
        if url[2] is IMG:
            with open(file_folder, 'wb') as img_file_save:
                for chunk in local_file.iter_content(BYTES_FOR_BLOCK):
                    img_file_save.write(chunk)
        else:
            with open(file_folder, 'w') as other_file_save:
                other_file_save.write(local_file.text)
        charging_bar.next()
    charging_bar.finish()
