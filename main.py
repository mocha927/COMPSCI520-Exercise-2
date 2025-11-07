# imports
import json
from glob import glob
import os

# tool to read JSON results from previous exercise and create modules for each
def read_results(directory='results', output_dir='scripts'):
    # create folder for scripts if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # create wildcard for json results
    results_dir_wc = os.path.join(directory, '*.json')

    for f in glob(results_dir_wc):
        # get file prefix
        pre = os.path.split(f.split('.json')[0])[-1]

        # get module name
        module_name = os.path.join(output_dir, pre)

        # create folder for module if it doesn't exist
        if not os.path.exists(module_name):
            os.mkdir(module_name)

        try:
            # open results file
            with open(f, 'r') as r_f:
                # create a dict from the file
                results = json.load(r_f)

                # module and test directory
                test_dir = os.path.join(module_name, 'tests')
                module_dir = os.path.join(module_name, pre)

                # make test directory for this set of candidates if not exists
                if not os.path.exists(test_dir):
                    os.mkdir(test_dir)

                # make test directory for this set of candidates if not exists
                if not os.path.exists(module_dir):
                    os.mkdir(module_dir)

                # write test script
                test_script_name = os.path.join(test_dir, f'test_{pre}.py')

                # write test_script to python file
                with open(test_script_name, 'w') as test_f:
                    test_f.write(results['test'])

                # write __init__.py into module folder
                module_init_path = os.path.join(module_dir, '__init__.py')
                with open(module_init_path, 'w') as module_f:
                    pass

                 # write __init__.py into test folder
                test_module_init_path = os.path.join(test_dir, '__init__.py')
                with open(test_module_init_path, 'w') as module_f:
                    pass

                # enumerate generated candidates
                for i, candidate in enumerate(results['candidates']):
                    try:
                        # get the function name of the candidate
                        func = candidate.split('def ')[-1].split('(')[0]

                        # get path for candidate and test code to save
                        candidate_path = os.path.join(module_dir, f'{func}_{i}.py')
                        test_candidate_path = os.path.join(test_dir, f'test_{func}_{i}.py')

                        # open new python file for candidate and write its contents
                        with open(candidate_path, 'w') as c_f:
                            c_f.write(candidate)

                        # open new python file for candidate test and write its contents
                        with open(test_candidate_path, 'w') as c_f:
                            c_f.write(
                                f"from tests.{os.path.split(test_script_name)[-1].split('.')[0]} import check\nfrom {pre}.{os.path.split(candidate_path)[-1].split('.')[0]} import {func}\ndef test_{func}_{i}():\n\tcheck({func})\n"
                            )
                    except Exception as e:
                        # print(traceback.print_exc(e))
                        # print(f"check({func})")
                        continue
        except Exception as e:
            continue

def execute_coverage_tests():
    from glob import glob
    import subprocess
    import os
    import sys

    # get all modules
    test_dirs = glob(os.path.join('scripts', '*'))

    # loop through all modules and run coverage tests on them
    for dir in test_dirs:
        # get module name
        module_name = os.path.split(dir)[-1]

        # get path to pytest
        pytest_exc = os.path.join(os.path.dirname(sys.executable), 'pytest')

        # get path for reports
        reports_path = os.path.join(os.getcwd(), 'reports', f"{module_name}_coverage.json")

        # run pytest with branch coverage included
        subprocess.call(
            [
                "cd",
                dir,
                "&",
                pytest_exc,
                "--timeout",
                "3",
                "--cov",
                module_name,
                "--cov-branch",
                "--cov-report",
                f"json:{reports_path}"
            ],
            shell=True
        )

def main():
    read_results()
    execute_coverage_tests()

if __name__ == "__main__":
    main()