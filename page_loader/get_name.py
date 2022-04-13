"""Get name."""
import os
from typing import Tuple, Union


def get_name(common_path: str) -> Tuple[Union[str], str]:
    """Get new formatted name.

    Args:
        common_path: path for file or url.

    Returns:
        tuple: (file name, file extension).
    """
    index_for_schema = common_path.find('/') + 2
    url_without_schema = common_path[index_for_schema:]
    body, file_extension = os.path.splitext(url_without_schema)
    for char in body:
        if not char.isalnum():
            body = body.replace(char, '-')
    return body, file_extension


def get_html_name(url: str) -> str:
    """Get name of html web page.

    Args:
        url: url of the web page.

    Returns:
        str: html file name.
    """
    return '{0}.html'.format(get_name(url)[0])


def get_folder_name(url: str) -> str:
    """Get folder name.

    Args:
        url: url of the web page.

    Returns:
        str: file folder name.
    """
    return '{0}_files'.format(get_name(url)[0])


def get_local_file_path(url: str, src: str) -> str:
    """Get file name with local path.

    Args:
        url: url of the downloaded web page.
        src: url for download local files.

    Returns:
        str: file name with local path.
    """
    file_name = get_name(src)
    return '{0}/{1}{2}'.format(get_folder_name(url), file_name[0], file_name[1])
