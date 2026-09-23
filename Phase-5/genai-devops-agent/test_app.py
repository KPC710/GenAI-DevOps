from app import add, multiply


def test_add():
    assert add(2, 3) == 5


def test_multiply():
    assert multiply(2, 3) == 6


def test_multiply_large_numbers():
    assert multiply(10, 5) == 50