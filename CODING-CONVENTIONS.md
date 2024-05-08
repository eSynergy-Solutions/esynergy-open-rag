# Coding Conventions

The following guidelines apply to code contributions to the Open RAG.

## Formatting

Open RAG uses [Black](https://github.com/psf/black) and [ISort](https://pycqa.github.io/isort/) to automatically format code. Please set up Black prior so that all your contributions to esynergy-open-rag will be formatted properly.

For instructions on using those tools with your IDE, see:

- [Black and ISort for VSCode](https://cereblanco.medium.com/setup-black-and-isort-in-vscode-514804590bf9)
- [Black and ISort for PyCharm](https://johschmidt42.medium.com/automate-linting-formatting-in-pycharm-with-your-favourite-tools-de03e856ee17)

## Linting

Open RAG uses [Flake8](https://flake8.pycqa.org/en/latest/) for code linting and type checking. Please set up Flake8 prior so that all your contributions to Open RAG will be linted properly.

For instructions on using Flake8 tool with VSCode:

- [Flake8 for VSCode](https://code.visualstudio.com/docs/python/linting)

For instructions on using Flake8 tool with PyCharm, see:

- [Installing third-party tools in PyCharm](https://www.jetbrains.com/help/pycharm/configuring-third-party-tools.html#remote-ext-tools)

## Pre-Commit Hooks

Open RAG uses [pre-commit](https://pre-commit.com/) to run Black, ISort, Flake8 before each commit.

To do so, install Open RAG's dependencies with `cd src/ && poetry install` and then install the hook by running `pre-commit install`

## Imports

Use absolute imports whenever possible. For example, instead of `from . import foo`, use `from esynergy_open_rag.config import foo`

To help with that, pre-commit hook will automatically fix relative imports to absolute imports.
