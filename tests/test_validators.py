import pytest

from app.validators import is_adult, is_valid_email, normalize_phone


@pytest.mark.parametrize("email, expected", [
    ("student@college.ru", True),
    ("student@college", False),
    ("student.college.ru", False),
])
def test_is_valid_email(email, expected):
    assert is_valid_email(email) is expected


@pytest.mark.parametrize("age, expected", [(17, False), (18, False), (45, True)])
def test_is_adult(age, expected):
    assert is_adult(age) is expected


def test_normalize_phone():
    assert normalize_phone("8 (999) 123-45-67") == "+79991234567"
