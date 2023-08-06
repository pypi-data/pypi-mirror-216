# bring-order
![GitHub Actions](https://github.com/Order-Team/bring-order/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/Order-team/bring-order/branch/main/graph/badge.svg?token=e8bdd46f-46b0-410c-820b-84ffca9ca53c)](https://codecov.io/gh/Order-team/bring-order)
[![GitHub](https://img.shields.io/github/license/Order-Team/bring-order)](LICENSE.md)

The tool is aimed at guiding data scientists with their analysis using custom widgets inside Jupyter Notebook.
User can import and prepare data for analysis, add limitations and perform deductive or inductive analysis.
Deductive analysis asks the user to set the hypothesis and null hypothesis, run their analysis, and confirm one of the hypotheses.
Inductive analysis is an option to perform explorative analysis and write notes about it.


## Documentation
* [Product backlog](https://docs.google.com/spreadsheets/d/1xqybqVAUIn4vhW-fBfhInQun7nY-uYH79M6l8oCiAzg/edit#gid=0)

* [Definition of Done](https://github.com/Order-Team/bring-order/blob/main/documentation/DoD.md)

* [Minutes of meetings](https://drive.google.com/drive/folders/1kwXCKbx7egHf8qYDIb4fRffNnad6Qd1t)

## Installation
### Installation from PyPi

### Linux

- If you don't have Jupyter Notebook installed, install it with
```bash
    pip install notebook
```

- If you don't have ipywidgets installed, install it with

```bash
    pip install ipywidgets
```

- If you have an old version of ipywidgets installed, upgrade it with

```bash
    pip install --upgrade ipywidgets
```

- Install bring-order extention:
```bash
    pip install bring-order
```

### Windows

- If you don't have Jupyter Notebook installed, install Anaconda with [Anaconda download](https://www.anaconda.com/download)

- Use Anaconda Powershell Prompt 

- If you don't have ipywidgets installed, install it with
```bash
    pip install ipywidgets
```
- If you have an old version of ipywidgets installed, upgrade it with
```bash
    pip install --upgrade ipywidgets
```

- Install bring-order extention:
```bash
    pip install bring-order
```

### MacOS
- If you don't have ipywidgets installed, install it with
```bash
    python3 -m pip install "ipywidgets"
```
- If you have an old version of ipywidgets installed, upgrade it with
```bash
    python3 -m pip install --upgrade ipywidgets
```
- Install bring-order extention:
```bash
    python3 -m pip install "bring-order"
```
### Usage
- Open Jupyter Notebook with
```bash
    jupyter notebook
```

- In Jupyter Notebook execute

``` 
    from bring_order import BringOrder  or  from bring_order import *
```
- Start using package by executing
``` 
    BringOrder()
```

- Make sure that your notebook is in Trusted state. Otherwise the widgets might not work correctly.

## Development

### Dependencies
- Clone the project and install dependencies in the main folder

```bash
    poetry install
```

### Testing
- Navigate to main folder and go to the virtual environment

```bash
    poetry shell
```

#### Run unit tests

```bash
    pytest tests
```

#### Run style check

```bash
    pylint bringorder
```

#### Run robot tests
- Make sure you have chromedriver installed and matching your Chrome version before running

```bash
    ./run_robot_tests.sh
```

- If the script won't run, give it execution rights first and try again
```bash
chmod +x run_robot_tests.sh
```

- If the first run fails, try once again. Sometimes there are some connection issues.
When you are done, you can exit the virtual environment with command

```bash
exit
```

#### Run tests with Invoke

- The previous tests can also be run using Invoke in poetry shell:

```bash
invoke tests
```
to run unit tests

```bash
invoke lint
```
to run pylint

```bash
invoke robottests
```
to run robottests

```bash
invoke alltests
```
to run all of the above
