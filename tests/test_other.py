from page_loader.get_name import get_folder_name, get_html_name, get_local_file_path

TEST_URL = 'https://ru.hexlet.io/courses'


def test_name():
    assert get_html_name(TEST_URL) == 'ru-hexlet-io-courses.html'
    assert get_folder_name(TEST_URL) == 'ru-hexlet-io-courses_files'
    assert get_local_file_path(TEST_URL, 'http://file_name') == 'ru-hexlet-io-courses_files/file-name.html'