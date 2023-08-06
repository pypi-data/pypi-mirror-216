"""Markdown tokens. These are the building blocks of a markdown document.

All functions in this module return a string that represents a markdown token.
"""

from typing import Dict, Iterable


def heading(
    text: str,
    level: int = 1,
) -> str:
    """Creates a heading with the given level by by prepending the text with `#`.

    Args:
        text (str): The text of the heading.
        level (int): The level of the heading. Must be greater than 0.

    Examples:
        >>> heading("Hello, world!")
        '# Hello, world!'
        >>> heading("Hello, world!", 2)
        '## Hello, world!'
    """  # noqa: E501
    if level < 1:
        raise ValueError("Level must be greater than 0.")

    return f"{'#' * level} {text}"


def h1(text: str) -> str:
    """Creates an h1."""
    return heading(text, 1)


def h2(text: str) -> str:
    """Creates an h2."""
    return heading(text, 2)


def h3(text: str) -> str:
    """Creates an h3."""
    return heading(text, 3)


def h4(text: str) -> str:
    """Creates an h4."""
    return heading(text, 4)


def h5(text: str) -> str:
    """Creates an h5."""
    return heading(text, 5)


def h6(text: str) -> str:
    """Creates an h6."""
    return heading(text, 6)


def paragraph(text: str) -> str:
    """Creates a paragraph. In fact, will just return the text.

    Args:
        text (str): The text of the paragraph.

    Examples:
        >>> paragraph("Hello, world!")
        'Hello, world!'
    """  # noqa: E501
    return text


def bold(text: str) -> str:
    """Creates bold text by wrapping the text with `**`.

    Args:
        text (str): The text to be set as bold.

    Examples:
        >>> bold("Hello, world!")
        '**Hello, world!**'
    """
    return f"**{text}**"


def italic(text: str) -> str:
    """Creates italic text by wrapping the text with `*`.

    Args:
        text (str): The text to be set as italic.

    Examples:
        >>> italic("Hello, world!")
        '*Hello, world!*'
    """
    return f"*{text}*"


def inline_code(text: str) -> str:
    """Creates code text by wrapping the text with backticks (``` ` ```).

    Args:
        text (str): The text to be set as code.

    Examples:
        >>> code("Hello, world!")
        '`Hello, world!`'
    """
    return f"`{text}`"


def quote(text: str) -> str:
    """Creates a quote by prepending the text with `>`.

    Args:
        text (str): The text of the quote.

    Examples:
        >>> quote("Hello, world!")
        '> Hello, world!'
    """
    return f"> {text}"


def strike_through(text: str) -> str:
    """Creates strike through text by wrapping the text with `~~`.

    Args:
        text (str): The text to be set as striked.

    Examples:
        >>> strike_through("Hello, world!")
        '~~Hello, world!~~'
    """
    return f"~~{text}~~"


def horizontal_ruler() -> str:
    """Creates a horizontal ruler using `---`.

    Examples:
        >>> horizontal_ruler()
        '---'
    """
    return "---"


def link(
    href: str,
    text: str | None = None,
) -> str:
    """Creates a link with `[text](href)` syntax.

    Args:
        href (str): The href of the link.
        text (str): The text to be shown as the link. If not provided, the href will be used instead.

    Examples:
        >>> link("https://example.com")
        '[https://example.com](https://example.com)'
        >>> link("https://example.com", "Example")
        '[Example](https://example.com)'
    """  # noqa: E501
    return f"[{text or href}]({href})"


def image(
    src: str,
    alt: str = "",
    mouseover: str = "",
):
    """Creates an image with `![alt](src "mouseover")` syntax.

    Args:
        src (str): The source of the image. Can be a path or a URL.
        alt (str): The alt text.
        mouseover (str): The mouseover text.

    Examples:
        >>> image("https://example.com/image.png")
        '![](https://example.com/image.png)'
        >>> image("https://example.com/image.png", "alt text", "mouseover text")
        '![alt text](https://example.com/image.png "mouseover text")'
    """
    if mouseover != "":
        mouseover = f' "{mouseover}"'

    return f"![{alt}]({src}{mouseover})"


def badge(
    img_src: str,
    href: str = "",
    alt: str = "",
    mouseover: str = "",
):
    """Creates a badge with `[![alt](img_src "mouseover")](href)` syntax.

    Args:
        img_src (str): The source of the badge image. Can be a path or a URL.
        href (str): The href of the badge.
        alt (str): The alt text.
        mouseover (str): The mouseover text.

    Examples:
        >>> badge("https://img", "https://link", "alt text", "mouseover")
        '[![alt text](https://img "mouseover")](https://link)'
    """
    img_str = image(img_src, alt, mouseover)

    return link(href, img_str)


def code_block(
    text: str,
    lang: str = "",
) -> str:
    r"""Creates a code block with triple backticks syntax.

    Args:
        text (str): The text of the code block.
        lang (str): The language of the code block.

    Examples:
        >>> code_block("print('Hello, world!')", "python")
        "```python\nprint('Hello, world!')\n```"
    """
    return f"```{lang}\n{text}\n```"


def unordered_list(*items: str) -> str:
    r"""Creates an unordered list by prepending each item with `- `.

    Args:
        items (Iterable[str]): Items to be listed.

    Examples:
        >>> unordered_list("Hello", "World")
        '- Hello\n- World'
    """
    return "\n".join(f"- {item}" for item in items)


def ordered_list(*items: str) -> str:
    r"""Creates an ordered list by prepending each item with `1. `.

    Args:
        items (Iterable[str]): Items to be listed.

    Examples:
        >>> ordered_list("Hello", "World")
        '1. Hello\n1. World'
    """
    return "\n".join(f"1. {item}" for item in items)


def table(*rows: Iterable[str]) -> str:
    r"""Creates a table from an iterable of rows with `|` syntax. Will separate the header and the body using `---`.

    Args:
        *rows (Iterable[str]): Unpacked iterable of rows. The first row is the header, and the rest are the body.

    Examples:
        >>> table(["name", "age"], ["John", "20"], ["Jane", "19"])
        'name | age\n--- | ---\nJohn | 20\nJane | 19'
    """  # noqa: E501
    rows_iter = iter(rows)
    header_row = next(rows_iter, None)

    if header_row is None:
        return ""

    header_row = list(header_row)

    first_row = next(rows_iter, None)

    if first_row is None:
        return ""

    header_str = " | ".join(header_row)
    divider_str = " | ".join("---" for _ in header_row)
    body_str = "\n".join((" | ".join(row) for row in (first_row, *rows_iter)))

    return "\n".join((header_str, divider_str, body_str))


def table_from_dicts(
    *dicts: Dict[str, str],
    header: Iterable[str] | None = None,
) -> str:
    r"""Creates a table from an iterable of dicts with `|` syntax. Will separate the header and the body using `---`.

    Args:
        *dicts (Dict[str, str]): Unpacked iterable of dicts. The keys of the first dict will be used as the header, and the values of each dict will be the body.
        header (Iterable[str] | None): Custom table header.

    Examples:
        >>> table_from_dicts({"name": "John", "age": "20"}, {"name": "Jane", "age": "19"})
        'name | age\n--- | ---\nJohn | 20\nJane | 19'
    """  # noqa: E501
    dicts_iter = iter(dicts)
    first_row = next(dicts_iter, None)

    if first_row is None:
        return ""

    header = header or list(first_row.keys())
    body = ((value for value in row.values()) for row in (first_row, *dicts_iter))

    return table(*(header, *body))


# short tokens
h = heading
p = paragraph
ul = unordered_list
ol = ordered_list
code = inline_code
hr = horizontal_ruler
img = image
