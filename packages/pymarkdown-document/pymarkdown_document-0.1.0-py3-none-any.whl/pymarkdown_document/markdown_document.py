"""Markdown document with line and span writing modes."""

from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Any, Callable, Concatenate, Dict, ParamSpec, TypeVar

from typing_extensions import Self

from pymarkdown_document import markdown_tokens as t


class WriteMode(str, Enum):
    """Enum representing the write mode of the document."""

    LINE = "line"
    SPAN = "span"


TSuper = TypeVar("TSuper", bound="MarkdownDocument")
TRetType = TypeVar("TRetType")
Params = ParamSpec("Params")


def attach_token_function(
    func: Callable[Params, str],
) -> Callable[Concatenate[TSuper, Params], TSuper]:
    """Function that turns a token into a method that returns the own [`MarkdownDocument`][pymarkdown_document.markdown_document.MarkdownDocument] instance.

    You are likely not using this as a decorator, but instead use it as a normal function.

    Args:
        func (Callable[P, str]): Token to be decorated. A token is a function that returns a string.

    Returns:
        Decorated function that will use
            [`add_content`][pymarkdown_document.markdown_document.MarkdownDocument.add_content]
            to add the content returned by the token to the document instance, and return the instance.
    """  # noqa: E501

    @wraps(func)
    def inner(
        self: TSuper,
        *args: Params.args,
        **kwargs: Params.kwargs,
    ) -> TSuper:
        self.add_content(func(*args, **kwargs))

        return self

    return inner


def token(
    func: Callable[Concatenate[TSuper, Params], str],
) -> Callable[Concatenate[TSuper, Params], TSuper]:
    """Decorates a method that implements a token.

    Args:
        func (Callable[Concatenate[TSuper, Params], str]): Method that implements a token.

    Returns:
        Decorated function that will use
            [`add_content`][pymarkdown_document.markdown_document.MarkdownDocument.add_content]
            to add the content returned by the token to the document instance, and return the instance.
    """  # noqa: E501

    @wraps(func)
    def inner(
        self: TSuper,
        *args: Params.args,
        **kwargs: Params.kwargs,
    ) -> TSuper:
        res = func(self, *args, **kwargs)
        self.add_content(res)

        return self

    return inner


def fixed_write_mode(mode: WriteMode):
    """Decorator to make an instance method of the [`MarkdownDocument`][pymarkdown_document.markdown_document.MarkdownDocument] class use a fixed write mode.

    Args:
        mode (WriteMode): Write mode to use.
    """  # noqa: E501

    def decorator(
        func: Callable[Concatenate[TSuper, Params], TRetType],
    ) -> Callable[Concatenate[TSuper, Params], TRetType]:
        @wraps(func)
        def inner(
            self: TSuper,
            *args: Params.args,
            **kwargs: Params.kwargs,
        ) -> TRetType:
            original_write_mode = self.write_mode
            self.write_mode = mode

            result = func(self, *args, **kwargs)

            self.write_mode = original_write_mode

            return result

        return inner

    return decorator


@dataclass
class MarkdownDocument:
    """A markdown document with line and span writing modes.

    # Line mode

    To write in line mode, use
        [`add_lines`][pymarkdown_document.markdown_document.MarkdownDocument.add_lines]
        or `lines`.
        Each line will be concatenated with the current content.

    # Span mode

    To write in span mode, use
        [`add_spans`][pymarkdown_document.markdown_document.MarkdownDocument.add_spans]
        or `spans`.
        Each span will be be joined to a single string and then concatenated with the current content.

    Args:
        content (str): Content of the markdown document.
        additional_tokens (dict[str, Any]): Dictionary of additional tokens that can be accessed via [`__getattr__`][pymarkdown_document.markdown_document.MarkdownDocument.__getattr__].
        write_mode ("line" | "span"): Writing mode of the document. Changes the behavior of the [`add_content`][pymarkdown_document.markdown_document.MarkdownDocument.add_content] method.
            [`add_lines`][pymarkdown_document.markdown_document.MarkdownDocument.add_lines] and
            [`add_spans`][pymarkdown_document.markdown_document.MarkdownDocument.add_spans]
            will not change behavior.
    """  # noqa: E501

    content: str = ""
    write_mode: WriteMode = field(default=WriteMode.LINE, init=False)
    additional_tokens: Dict[str, Any] = field(default_factory=dict)

    def line_mode(self) -> Self:
        """Sets the writing mode to `line` mode."""
        self.write_mode = WriteMode.LINE

        return self

    def span_mode(self) -> Self:
        """Sets the writing mode to `span` mode."""
        self.write_mode = WriteMode.SPAN

        return self

    def toggle_write_mode(self) -> Self:
        """Toggles the writing mode between `line` and `span`."""
        self.write_mode = (
            WriteMode.LINE if self.write_mode == WriteMode.SPAN else WriteMode.SPAN
        )  # noqa: E501

        return self

    def add_content(self, other_content: str) -> Self:
        """Concatenate `other_content` with the current content.

        If the current content is empty, `other_content` will be set as the content.
            Otherwise, `other_content` will be concatenated with the current content based on the rule below.

        If the writing mode is `line`, `other_content` will be prepended with double line breaks and concatenated with the current content.
            Otherwise, `other_content` will be concatenated with the current content with no changes.

        Args:
            other_content (str): Content to be added.

        Returns:
            The document instance.
        """  # noqa: E501
        if self.content == "":
            self.content += other_content

        else:
            if self.write_mode == "line":
                other_content = "\n\n" + other_content

            self.content += other_content

        return self

    @fixed_write_mode(WriteMode.LINE)
    def add_lines(self, *lines: str) -> Self:
        """Joins the lines with double line breaks and concatenate with the document.

        Args:
            *lines (str): Unpacked iterable of lines to be appended.

        Returns:
            The document instance.
        """
        joined_lines = "\n\n".join(lines)
        self.add_content(joined_lines)

        return self

    @fixed_write_mode(WriteMode.LINE)
    def add_spans(self, *spans: str) -> Self:
        """Joins the spans and concatenate with the document.

        Args:
            *spans (str): Unpacked iterable of spans to be joined.

        Returns:
            The document instance.
        """
        joined_spans = "".join(spans)
        self.add_content(joined_spans)

        return self

    def edit_content(
        self,
        *functions: Callable[[str], str],
    ) -> Self:
        """Replaces the content of the document with the result of the function.

        Args:
            *functions ((str -> str)): Unpacked iterable of functions that takes in the content of the document and returns new content.

        Returns:
            The document instance.
        """  # noqa: E501
        for function in functions:
            self.content = function(self.content)

        return self

    def __getattr__(self: TSuper, attr: str) -> Callable[..., TSuper]:
        """Shorthand for using the fluent API to add tokens to the document.

        Args:
            attr (str): Name of the token to be added (refer to [`markdown_tokens`][pymarkdown_document.markdown_tokens]).

        Returns:
            A function that takes the arguments of the token and returns the document instance.
        """  # noqa: E501

        def inner(*args, **kwargs) -> TSuper:
            value: str = self.additional_tokens[attr](*args, **kwargs)

            self.add_content(value)

            return self

        return inner

    def __str__(self) -> str:
        """Returns the content of the document."""
        return self.content

    lines = add_lines
    spans = add_spans
    add = add_content

    # shortcuts for the tokens
    heading = attach_token_function(t.heading)
    h1 = attach_token_function(t.h1)
    h2 = attach_token_function(t.h2)
    h3 = attach_token_function(t.h3)
    h4 = attach_token_function(t.h4)
    h5 = attach_token_function(t.h5)
    h6 = attach_token_function(t.h6)
    paragraph = attach_token_function(t.paragraph)
    bold = attach_token_function(t.bold)
    italic = attach_token_function(t.italic)
    inline_code = attach_token_function(t.inline_code)
    quote = attach_token_function(t.quote)
    strike_through = attach_token_function(t.strike_through)
    horizontal_ruler = attach_token_function(t.horizontal_ruler)
    link = attach_token_function(t.link)
    image = attach_token_function(t.image)
    badge = attach_token_function(t.badge)
    code_block = attach_token_function(t.code_block)
    unordered_list = attach_token_function(t.unordered_list)
    ordered_list = attach_token_function(t.ordered_list)
    table = attach_token_function(t.table)
    table_from_dicts = attach_token_function(t.table_from_dicts)

    h = heading
    p = paragraph
    ul = unordered_list
    ol = ordered_list
    code = inline_code
    hr = horizontal_ruler
    img = image
