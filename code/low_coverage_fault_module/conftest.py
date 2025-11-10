import pytest
from _pytest.runner import pytest_runtest_makereport as _makereport

assertion_count = 0

@pytest.hookimpl(optionalhook=True)
def pytest_json_runtest_metadata(item, call):
    report = {}
    
    if call.when != 'call':
        return report
    
    if hasattr(item, 'function') and hasattr(item.function, 'test_accuracy'):
        report['test_accuracy'] = item.function.test_accuracy
        report['name'] = item.function.__name__
        
    return report