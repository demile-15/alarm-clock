import pytest
from project import timer, string_to_sec

def test_string_to_sec():
    assert string_to_sec("00:00:04") == 4
    assert string_to_sec("00:00:00") == 0
    assert string_to_sec("01:39:45") == 5985