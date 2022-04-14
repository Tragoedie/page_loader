"""This is a module to test programm for error raising."""

import os
import requests_mock
import pytest
from page_loader.download import ExpectedError, download
import tempfile

UNACCESSABLE_RIGHTS = 000
ACCESSABLE_RIGHTS = 777
NETWORK_ERROR_CODE = 404
TEST_URL = 'https://wrong_adress.ru'


def test_html_download_error_404():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(TEST_URL, status_code=NETWORK_ERROR_CODE)
        with pytest.raises(ExpectedError, match=r".*404.*"):
            download(TEST_URL, temp_dir)


def test_403_error():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(ExpectedError) as exception_info:
            url = 'https://en.wikipediaa.com/'
            download(url, tmp_dir)
        assert '403 Client Error: Forbidden for url' in str(exception_info.value)


def test_download_wrong_path(tmp_path):
    wrong_folder_path = os.path.join(tmp_path, '/wrong_folder_path')
    with pytest.raises(ExpectedError):
        download(TEST_URL, wrong_folder_path)
