from page_loader.download import get_response
from page_loader.html import prepare_links
from bs4 import BeautifulSoup

TEST_URL = 'https://ru.hexlet.io/courses'


def test_html(requests_mock, tmpdir, before_replace, after_replace):
    requests_mock.get(TEST_URL, text=before_replace)
    url_for_download, html = prepare_links(
        get_response(TEST_URL).text,
        TEST_URL,
    )
    soup = BeautifulSoup(after_replace, 'html.parser')
    assert url_for_download == [
        ('https://ru.hexlet.io/assets/professions/nodejs.png',
         'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png')
    ]
    assert html == soup.prettify('utf-8')
