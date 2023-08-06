from ..gui.helpers import file


def test_file_existence():
    assert file.exists(), "File must exist"


def test_file_is_file():
    assert file.is_file(), "File must be a file"
