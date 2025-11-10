from tests.test_cot_results_llama_52 import check
from low_coverage_code.below_threshold_1 import below_threshold
import pytest

def test_below_threshold_1():
	correct, total = check(below_threshold)
	test_below_threshold_1.test_accuracy = float(correct/(1e-8 + total))