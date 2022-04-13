"""Replace links."""

from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from page_loader.get_name import get_local_file_path

IMG = 'img'
SRC = 'src'
LINK = 'link'
HREF = 'href'
SCRIPT = 'script'

DICT_FOR_LINK = {IMG: SRC, SCRIPT: SRC, LINK: HREF}


def is_local_file(src: str, url: str) -> bool:
    """Check if url of download file is local.

    Args:
        src: link to the file in html.
        url: url of the downloaded web page.

    Returns:
        bool: local or not.
    """
    domain = urlparse(url).netloc
    return urlparse(src).netloc in domain


def replace_links(html_path: str, url: str) -> List[tuple]:
    """Replace links in downloaded html page from web links to local files.

    Args:
        html_path: place, where the downloaded html file is located.
        url: url of the web page.

    Returns:
        array of tuple:
        1) tag_path - url for download file,
        2) path_for_replace - local path for downloaded file,
        2) tag.name - name of tag.
    """
    with open(html_path) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    urls = []
    for tag in soup.find_all(DICT_FOR_LINK.keys()):
        tag_path = tag.get(DICT_FOR_LINK[tag.name])
        if tag_path is None or is_local_file(tag_path, url) is False:
            continue
        src_parse = urlparse(tag_path)
        if src_parse.netloc == '':
            url_parse = urlparse(url)
            tag_path = '{0}://{1}{2}'.format(
                url_parse.scheme,
                url_parse.netloc,
                tag_path,
            )
        path_for_replace = get_local_file_path(url, tag_path)
        tag[DICT_FOR_LINK[tag.name]] = path_for_replace
        urls.append((tag_path, path_for_replace, tag.name))
        with open(html_path, 'w') as new_html:
            new_html.write(soup.prettify())
    return urls
