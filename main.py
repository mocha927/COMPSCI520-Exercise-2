# imports
import json
from glob import glob
import os
import shutil

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

        # add conftest and .ini file to module
        shutil.copy('conftest.py', os.path.join(module_name, "conftest.py"))
        shutil.copy('pytest.ini', os.path.join(module_name, "pytest.ini"))

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

                # parse test suite into array of tuples
                tests = list(
                    zip(
                        eval(results['test'].split('inputs = ')[-1].split('\n')[0]),
                        eval(results['test'].split('results = ')[-1].split('\n')[0])
                    )
                )

                # write test_script to python file
                with open(test_script_name, 'w') as test_f:
                    test_f.write("import pytest")
                    test_f.write(results['test'].
                        replace("assert ", "return ").
                        replace("def check(candidate):",
                            "def check(candidate):\n    correct = 0\n"
                        ).
                        replace("assertion(candidate(*inp), exp, 0)",
                            "correct += assertion(candidate(*inp), exp, 0)\n    return correct, len(results)"
                        )
                    )

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
                                f"from tests.{os.path.split(test_script_name)[-1].split('.')[0]} import check\nfrom {pre}.{os.path.split(candidate_path)[-1].split('.')[0]} import {func}\nimport pytest\n\ndef test_{func}_{i}():\n\tcorrect, total = check({func})\n\ttest_{func}_{i}.test_accuracy = float(correct/(1e-8 + total))"
                            )
                    except Exception as e:
                        # print(traceback.print_exc(e))
                        # print(f"check({func})")
                        continue
        except Exception as e:
            continue

import subprocess
import sys

def pycov_test_module(
    project_dir: str,
    module_name: str,
    output_file_path: str,
    executable: str=os.path.join(os.path.dirname(sys.executable), 'pytest'),
):
    # run pytest with branch coverage included
    subprocess.call(
        [
            "cd",
            project_dir,
            "&",
            executable,
            "--timeout",
            "3",
            "--cov",
            module_name,
            "--cov-branch",
            "--cov-report",
            f"markdown:{output_file_path}",
            "--cov-report",
            "term-missing",
            "--json-report",
            "--json-report-file",
            f"{output_file_path.split('.')[0]+'_acc.json'}"
        ],
        shell=True
    )

# Number of tests passed, Line coverage and branch coverage (if the tool supports it for your language).
# - A one-line interpretation (e.g., “low branch coverage due to untested error path”).
# 3. Include a single summary table across all problems (problem → line %, branch %, notes).

def execute_coverage_tests(scripts_path='scripts', reports_path='reports'):
    from glob import glob
    import os

    # get all modules
    test_dirs = glob(os.path.join(scripts_path, '*'))

    # create reports directory if not existing
    if not os.path.exists(reports_path):
        os.mkdir(reports_path)

    # loop through all modules and run coverage tests on them
    for d in test_dirs:
        # get module name
        module_name = os.path.split(d)[-1]

        # get path for reports
        report_path = os.path.join(os.getcwd(), 'reports', f"{module_name}_coverage.md")

        # run pytest coverage test and write results to output path
        pycov_test_module(d, module_name, report_path)

def mrkd2json(inp):
    lines = inp.split('\n')
    ret=[]
    keys=[]
    for i,l in enumerate(lines):
        if i==0:
            keys=[_i.strip() for _i in l.split('|')]
        elif i==1: continue
        else:
            ret.append({keys[_i]:v.strip() for _i,v in enumerate(l.split('|')) if  _i>0 and _i<len(keys)-1})
    return ret

def get_coverages(reports_path='reports', results_path="results", output_path="coverage.xlsx"):
    from glob import glob
    import os
    import json
    import pandas as pd
    import numpy as np
    import json

    # get paths to all json results
    results_dir = glob(os.path.join(reports_path, "*coverage.md"))

    # test results
    test_results = []

    # loop through all json results and append their coverages
    for res in results_dir:
        # get module name
        pre = os.path.split(res)[-1].split('_coverage.')[0]

        # new test result
        test_result = {}

        # get corresponding accuracy json file
        acc = res.split('.')[0] + '_acc.json'

        # create module stats
        test_result[pre] = {}

        # open file and add coverage and accuracy for current result
        with open(res, "r") as f:
            # add coverages for current module
            for stats in mrkd2json(f.read())[1:-2]:
                name = ''.join(stats['Name'].split('\\')).split(pre)[-1].split('.')[0]
                if test_result[pre].get(name) is None:
                    test_result[pre][name] = {}
                    test_result[pre][name]['cover'] = float(stats['Cover'].split("%")[0]) / 100
                    test_result[pre][name]['branch'] = 1 - float(int(stats['BrPart']) / (1e-8 + int(stats['Branch'])))
        with open(acc, "r") as f:
            # load json report
            j = json.load(f)
            # add accuracy for current module
            for t in j['tests']:
                if t.get('metadata') is not None:
                    # get test name
                    name = t['metadata']['name'].split('test_')[-1]

                    # append accuracy
                    if test_result[pre].get(name) is not None:
                        test_result[pre][name]['accuracy'] = t['metadata']['test_accuracy']

        # get test with highest accuracy
        test_names = []

        for (name, stats) in test_result[pre].items():
            if stats.get('accuracy') is not None:
                test_names.append((name, stats['accuracy']))

        if len(test_names) == 0:
            continue

        best_test_name = max(test_names, key=lambda x: x[1])[0]

        # add test result
        test_result = {"result_name": pre, "name": best_test_name, **test_result[pre][best_test_name]}
        test_results.append(test_result)
    
    for i in range(len(test_results)):
        res = test_results[i]

        # load json results
        json_results = os.path.join(results_path, f'{res['result_name']}.json')
        with open(json_results, 'r') as f:
            j = json.load(f)
            idx = int(res['name'].split('_')[-1])

            # append prompt and code to results
            test_results[i] = {
                'prompt': j['prompt'],
                'code': j['candidates'][idx],
                **res
            }

    # save to excel sheet
    pd.DataFrame(test_results).to_excel(output_path)

    # sort by branch cover ascending
    metric = np.argsort([
        res['branch']
        for res in test_results
    ])

    # get top two
    top_two = metric[:2]

    # dump low coverage results
    with open('low_coverage_results.json', 'w') as f:
        json.dump([test_results[top_two[0]],
            test_results[top_two[1]]], f)

def main():
    # read_results()
    # execute_coverage_tests()
    get_coverages()

if __name__ == "__main__":
    main()