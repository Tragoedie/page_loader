from page_loader.download import ExpectedError, download, download_local_files

import requests_mock
import tempfile
import os
import pytest


TEST_URL = 'https://ru.hexlet.io/courses'
IMG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
ERROR_CODE = 404


with open('tests/fixtures/before.html', 'r') as before_html:
    before_replace_links = before_html.read()
with open('tests/fixtures/after.html', 'r') as after_html:
    after_replace_links = after_html.read()
with open('tests/fixtures/image_file.png', 'rb') as image_file:
    image_content = image_file.read()


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(TEST_URL, text=before_replace_links)
            mock_request.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
            html_file_path = download(TEST_URL, temp_dir)
            assert html_file_path == temp_dir + '/ru-hexlet-io-courses.html'
            img_filepath = os.path.join(temp_dir, 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png')
            with open(img_filepath, 'rb') as img_file:
                img_result = img_file.read()
            assert img_result == image_content
            with open(html_file_path, 'r') as html:
                content = html.read()
            assert content == after_replace_links
            assert os.path.exists(html_file_path)
            assert os.path.isfile(html_file_path)


def test_download_local_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
            img_path = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
            img_file_path = os.path.join(temp_dir, img_path)
            url = [(IMG_URL, img_file_path)]
            download_local_files(url, temp_dir)
            with open(img_file_path, 'rb') as img_file:
                img_result = img_file.read()
            assert img_result == image_content


def test_html_download_error_404():
    with pytest.raises(ExpectedError):
        with tempfile.TemporaryDirectory() as temp_dir:
            with requests_mock.Mocker() as mock_request:
                mock_request.get(TEST_URL, status_code=ERROR_CODE)
                download(TEST_URL, temp_dir)


def test_download_wrong_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        wrong_folder_path = os.path.join(temp_dir, '/wrong_folder_path')
        with pytest.raises(ExpectedError):
            download(TEST_URL, wrong_folder_path)



