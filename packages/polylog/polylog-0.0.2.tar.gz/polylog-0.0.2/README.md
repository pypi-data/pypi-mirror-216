# PolyLog

PolyLog is a custom logging package designed to support your application development process. Built with versatility in mind, this package provides comprehensive, formatted logging in Python. It includes features such as:

- Customizable formatting
- Thread-safe logging
- Trace and Span ID integration
- Color-coded log levels
- Optional local log file storage

This package forms part of a larger multi-language (polylog) logging framework, with companion modules in Go, Rust, and TypeScript.

## Installation

To install PolyLog, you can simply use pip:

```bash
pip install polylog
```

## Usage

Here is a basic usage example:

```python
from polylog import setup_logger

# Set up the logger
logger = setup_logger(__name__)

# Use the logger
logger.info("This is an information message")
logger.error("This is an error message")
```

In this example, `setup_logger` is a function that sets up the logger and returns it. You can then use methods like `logger.info` and `logger.error` to log messages.

## Contact

If you have any questions, feel free to reach out at [GitHub](https://github.com/lvlcn-t/polylog/issues).

## License

This project is licensed under the terms of the MIT license.

