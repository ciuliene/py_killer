# PyKiller

[![Python application](https://github.com/ciuliene/py_killer/actions/workflows/merge.yml/badge.svg?branch=main)](https://github.com/ciuliene/py_killer/actions/workflows/merge.yml)

Python script to list and kill processes

## Installation

Create virtual environment:

```
python -m venv <virtual-environment-name>
```

Activate virtual environment:

```
source <virtual-environment-name>/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

## Usage

To list all running processes with relative _pid_:

```
python main.py -l
```

To kill a process:

```
python main.py -n <process-name>
```

Note: the process name must be a name in the list obtained from the previous command.
