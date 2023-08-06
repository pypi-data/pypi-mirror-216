"""Write markdown documents with a fluent API."""

from . import markdown_tokens
from .markdown_document import (
    MarkdownDocument,
    WriteMode,
    attach_token_function,
    fixed_write_mode,
    token,
)


__all__ = (
    "markdown_tokens",
    "MarkdownDocument",
    "attach_token_function",
    "fixed_write_mode",
    "token",
    "WriteMode",
)
