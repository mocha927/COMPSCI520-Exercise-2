from tests.test_cot_results_llama_80 import check
from low_coverage_code.is_happy_2 import is_happy
import pytest

def test_is_happy_2():
	correct, total = check(is_happy)
	test_is_happy_2.test_accuracy = float(correct/(1e-8 + total))

def test_short_sequence_returns_false():
    assert is_happy("ab") is False

def test_no_matches_returns_false():
    assert is_happy([1, 2, 3, 4, 5]) is False

def test_custom_sequence_returns_true():
    class HappySeq:
        def __len__(self):
            return 5
        def __getitem__(self, idx):
            if isinstance(idx, slice):
                start = idx.start
                return self[start + 1]
            return f"item{idx}"
    s = HappySeq()
    assert is_happy(s) is True