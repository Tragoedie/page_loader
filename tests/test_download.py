import pytest
from page_loader.download_function import download_html, download_local_files, download
from page_loader.get_name import get_folder_name, get_html_name, get_local_file_path
import requests_mock
import tempfile
import os

URL = 'https://ru.hexlet.io/courses'
IMG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'

with open('tests/fixtures/before.html', 'r') as before_html:
    before_replace_links = before_html.read()
with open('tests/fixtures/after.html', 'r') as after_html:
    after_replace_links = after_html.read()
with open('tests/fixtures/image_file.png', 'rb') as image_file:
    image_content = image_file.read()


def test_download_html():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(URL, text=before_replace_links)
            html_file = download_html(URL, temp_dir)
            assert html_file == temp_dir + '/ru-hexlet-io-courses.html'
            with open(html_file, 'r') as html:
                content = html.read()
                assert content == before_replace_links


def test_download_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
            img_filepath = os.path.join(temp_dir, 'ru-hexlet-io-assets-professions-nodejs.png')
            download_local_files([(IMG_URL, img_filepath, 'img')], temp_dir)
            assert os.path.exists(img_filepath)
            assert os.path.isfile(img_filepath)
            with open(img_filepath, 'rb') as img_file:
                img_result = img_file.read()
            assert img_result == image_content


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(URL, text=before_replace_links)
            mock_request.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
            html_file_path = download(URL, temp_dir)
            assert html_file_path == temp_dir + '/ru-hexlet-io-courses.html'
            with open(html_file_path, 'r') as html:
                content = html.read()
            assert content == after_replace_links


def test_name():
    assert get_html_name(URL) == 'ru-hexlet-io-courses.html'
    assert get_folder_name(URL) == 'ru-hexlet-io-courses_files'
    assert get_local_file_path(URL, 'http://file_name') == 'ru-hexlet-io-courses_files/file-name'
