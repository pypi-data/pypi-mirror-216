# pymarkdown-document

> Write markdown documents with a fluent API.

[![Documentation Status](https://readthedocs.org/projects/pymarkdown-document/badge/?version=latest)](https://pymarkdown-document.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/demetrius-mp/pymarkdown-document/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/demetrius-mp/pymarkdown-document/actions/workflows/pipeline.yaml)
[![codecov](https://codecov.io/gh/demetrius-mp/pymarkdown-document/branch/main/graph/badge.svg?token=PXK3OH6R8Q)](https://codecov.io/gh/demetrius-mp/pymarkdown-document)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![Docstring Style](https://img.shields.io/badge/%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Installation

You can install with `pip`, `poetry`, or any other package manager:

```bash
pip install pymarkdown-document
```

## Usage

> For a more complete example, see [docs/usage.md](docs/usage.md).

```python
from pymarkdown_document import MarkdownDocument

document = MarkdownDocument()

document = (
    document
    .h1("pymarkdown-document")
    .quote("Write markdown documents with a fluent API.")
    .h2("Installation")
    .p("You can install with ")
    .span_mode()
    .code("pip")
    .p(", ")
    .code("poetry")
    .p(", or any other package manager:")
    .line_mode()
    .code_block("pip install pymarkdown-document", "bash")
)
```

## License

This project is licensed under the terms of the [GPL-3.0-only license](https://spdx.org/licenses/GPL-3.0-only.html).