import pytest
from low_coverage_code.below_threshold_1 import below_threshold

def test_non_list_input_raises():
    with pytest.raises(ValueError):
        below_threshold("not a list", 5)

def test_empty_list_returns_false():
    assert below_threshold([], 5) is False

def test_single_element_ge_threshold_returns_false():
    assert below_threshold([5], 5) is False

def test_later_element_ge_threshold_returns_false():
    assert below_threshold([1, 5, 2], 4) is False

def test_all_elements_below_threshold_returns_true():
    assert below_threshold([0, 1, 2, 3], 5) is True