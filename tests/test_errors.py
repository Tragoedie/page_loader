"""This is a module to test programm for error raising."""

import os
import requests_mock
import pytest
from page_loader.download import ExpectedError, download
import tempfile

ERROR_CODE = 404
TEST_URL = 'https://ru.hexlet.io/les'


def test_html_download_error_404():
    with pytest.raises(ExpectedError):
        with tempfile.TemporaryDirectory() as temp_dir:
            with requests_mock.Mocker() as mock_request:
                mock_request.get(TEST_URL, status_code=ERROR_CODE)
                download(TEST_URL, temp_dir)


def test_403_error():
    with pytest.raises(ExpectedError) as err_info:
        with tempfile.TemporaryDirectory() as temp_dir:
            download(TEST_URL, temp_dir)
        assert '403 Client Error: Forbidden for url' in str(err_info.value)


def test_download_wrong_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        wrong_folder_path = os.path.join(temp_dir, '/wrong_folder_path')
        with pytest.raises(ExpectedError):
            download(TEST_URL, wrong_folder_path)
