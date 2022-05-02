"""Replace links."""

from typing import Any, List, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from page_loader.names import get_local_file_path

IMG = 'img'
SRC = 'src'
LINK = 'link'
HREF = 'href'
SCRIPT = 'script'

LINKS = {IMG: SRC, SCRIPT: SRC, LINK: HREF}


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


def prepare_links(html_response: Any, url: str) -> Tuple[List[tuple], Any]:
    """Replace links in downloaded html page from web links to local files.

    Args:
        html_response: place, where the downloaded html file is located.
        url: url of the web page.

    Returns:
        array of tuple:
        1) tag_path - url for download file,
        2) path_for_replace - local path for downloaded file,
        2) tag.name - name of tag.
    """
    soup = BeautifulSoup(html_response, 'html.parser')
    urls = []
    for tag in soup.find_all(LINKS.keys()):
        tag_path = tag.get(LINKS[tag.name])
        if tag_path is None or is_local_file(tag_path, url) is False:
            continue
        src_parse = urlparse(tag_path)
        if not src_parse.netloc:
            url_parse = urlparse(url)
            tag_path = '{0}://{1}{2}'.format(
                url_parse.scheme,
                url_parse.netloc,
                tag_path,
            )
        path_for_replace = get_local_file_path(url, tag_path)
        tag[LINKS[tag.name]] = path_for_replace
        urls.append((tag_path, path_for_replace))
    return urls, soup.prettify()
