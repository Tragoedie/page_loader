"""This is a module to test programm for error raising."""

import os
import requests_mock
import pytest
from page_loader.download import ExpectedError, download
import tempfile

ERROR_CODE = 404
TEST_URL = 'https://ru.hexlet.io/les'


def test_html_download_error_404():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock_request:
            mock_request.get(TEST_URL, status_code=ERROR_CODE)
            with pytest.raises(ExpectedError):
                download(TEST_URL, temp_dir)


def test_download_wrong_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        wrong_folder_path = os.path.join(temp_dir, '/wrong_folder_path')
        with pytest.raises(ExpectedError):
            download(TEST_URL, wrong_folder_path)
