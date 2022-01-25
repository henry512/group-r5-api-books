# Mutant API - Linux Installation

## Prerequisites

- [`Python 3.8.5`](https://www.python.org/downloads/release/python-385/)
- [`OS Linux - Ubuntu <optional>`](http://releases.ubuntu.com/18.04/)

## Installation

Create a new python environment in `.env` folder:

```bash
pip3 install virtualenv
virtualenv env --python=python3.8
```

Set the new python environment:

```bash
source .env/bin/activate
```

Update `pip` package and install requirements for development environment:

```bash
pip install --upgrade pip
pip install -r requirements/development.txt
```