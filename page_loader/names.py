"""Get name."""

import pathlib
import re
from urllib.parse import urlparse


def get_name(common_path: str) -> str:
    """Get new formatted name.

    Args:
        common_path: path for file or url.

    Returns:
        str: string.
    """
    prefix = urlparse(common_path).scheme
    body = re.sub(r'^{0}://'.format(prefix), '', common_path)
    return re.sub(r'[^a-zA-Z\d]', '-', body)


def get_html_name(url: str) -> str:
    """Get name of html web page.

    Args:
        url: url of the web page.

    Returns:
        str: html file name.
    """
    return '{0}.html'.format(get_name(url))


def get_folder_name(url: str) -> str:
    """Get folder name.

    Args:
        url: url of the web page.

    Returns:
        str: file folder name.
    """
    return '{0}_files'.format(get_name(url))


def get_local_file_path(url: str, src: str) -> str:
    """Get file name with local path.

    Args:
        url: url of the downloaded web page.
        src: url for download local files.

    Returns:
        str: file name with local path.
    """
    if not urlparse(src).netloc:
        src = '{0}{1}'.format(urlparse(url).netloc, src)
    file_extension = pathlib.Path(src).suffix
    if not file_extension:
        file_extension = '.html'
    body = re.sub(r'{0}$'.format(file_extension), '', src)
    return '{0}/{1}{2}'.format(
        get_folder_name(url),
        get_name(body),
        file_extension,
    )
