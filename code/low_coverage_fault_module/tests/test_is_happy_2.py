from tests.test_cot_results_llama_80 import check
from low_coverage_code.is_happy_2 import is_happy
import pytest

def test_is_happy_2():
	correct, total = check(is_happy)
	test_is_happy_2.test_accuracy = float(correct/(1e-8 + total))