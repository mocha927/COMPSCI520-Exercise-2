# COMPSCI520-Exercise-2

## Description

This repository contains the source code to generated coverage reports for the llm-generated code in json format from Exercise-1 which I've included in the [results](./results/) directory.

The main script will load the json files in [results](./results/), create coverage reports in markdown format using the pytest-cov tool and record the percentage of passed tests from each llm-generated candidate in json format in the [reports](./reports/) folder. The main script will also create a 'scripts' directory locally which create project directories with tests for each set of llm-generated code which are used by pytest-cov to generate the coverage reports. Finally, two llm-generated functions corresponding to the minimum coverage will be saved into the [code](./code/) directory.

Inside the code directory, there are the project directories for the llm-generated test-suites for the two selected functions. [./code/low_coverage_module](./code/low_coverage_module/) corresponds to just the enhanced test-suite and [./code/low_coverage_fault_module](./code/low_coverage_fault_module/) has a bug introduced into each function as well.

## Installation

run ```pip install -r requirements.txt``` to install python packages

## How to Run

```python main.py``` will run through all the steps to generate the test code, coverage reports, and two lowest coverage functions as described.