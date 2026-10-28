import time
import pytest

@pytest.mark.parametrize("i", range(8))
def test_slow_check(i):
    time.sleep(2.5)
    assert i >= 0
