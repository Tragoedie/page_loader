from page_loader.download import ExpectedError, download, download_local_files

import requests_mock
import tempfile
import os
import pathlib
import pytest

TEST_URL = 'https://ru.hexlet.io/courses'
IMG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
ERROR_CODE = 404


@pytest.fixture()
def before_replace():
    with open('tests/fixtures/before.html', 'r') as before:
        data = before.read()
    return data


@pytest.fixture()
def after_replace():
    with open('tests/fixtures/after.html', 'r') as after:
        data = after.read()
    return data


@pytest.fixture()
def image_content():
    with open('tests/fixtures/image_file.png', 'rb') as img:
        content = img.read()
    return content


def test_download(before_replace, after_replace, image_content, requests_mock, tmpdir):
    """Test download function: check downloaded html file.

    Args:
        requests_mock: mock for HTTP request.
        tmp_path: temporary path for testing.
    """
    requests_mock.get(TEST_URL, text=before_replace)
    requests_mock.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
    html_file_path = download(TEST_URL, tmpdir)
    assert html_file_path == tmpdir + '/ru-hexlet-io-courses.html'
    img_filepath = os.path.join(
        tmpdir,
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png',
    )
    with open(img_filepath, 'rb') as img_file:
        img_result = img_file.read()
    assert img_result == image_content
    with open(html_file_path, 'r') as html:
        content = html.read()
    assert content == after_replace
    assert os.path.exists(html_file_path)
    assert os.path.isfile(html_file_path)


def test_download_local_files(image_content, requests_mock, tmpdir):
    requests_mock.get(IMG_URL, content=image_content, headers={'content-type': 'png'})
    img_path = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
    img_file_path = os.path.join(tmpdir, img_path)
    pathlib.Path(os.path.join(tmpdir, 'ru-hexlet-io-courses_files/')).mkdir(exist_ok=True)
    url = [(IMG_URL, img_file_path)]
    download_local_files(url, tmpdir)
    with open(img_file_path, 'rb') as img_file:
        img_result = img_file.read()
    assert img_result == image_content


def test_html_download_error_404(requests_mock, tmpdir):
    with pytest.raises(ExpectedError):
        requests_mock.get(TEST_URL, status_code=ERROR_CODE)
        download(TEST_URL, tmpdir)


def test_download_wrong_path(tmpdir):
    wrong_folder_path = os.path.join(tmpdir, '/wrong_folder_path')
    with pytest.raises(ExpectedError):
        download(TEST_URL, wrong_folder_path)
