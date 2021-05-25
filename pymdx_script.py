"""Python-Markdown extension converting the `%[]()` markers into `<script>` tags.

`pip install git+https://github.com/carnarez/pymdx-script` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

Example
-------
```python
import markdown
provided = "%[Run script.js (d3.js)](/wherever/script.js)"
rendered = markdown.markdown(provided, extensions=[ScriptExtension()])
expected = '<p id="run-scriptjs-d3js"><script src="/wherever/script.js"></script></p>'
assert rendered == expected
```
"""

import re
import typing

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class ScriptPreprocessor(Preprocessor):
    """Preprocessor to catch and replace the `%[]()` markers."""

    def __init__(self, md: Markdown):
        """All methods inherited, but the `run()` one below.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.
        """
        super().__init__(md)

    @staticmethod
    def html(id_: str, src: str) -> str:
        """Return the HTML block including the parameters.

        At the moment, the returned HTML is:

        ```html
        <p id=""><script src=""></script></p>
        ```

        Parameters
        ----------
        id_ : str
            The `id` of the HTML elements. To be fetched via `.getElementById()`.
        src : str
            The path to the script.

        Returns
        -------
        : str
            HTML elements.
        """
        return f'<p id="{id_}"><script src="{src}"></script></p>'

    @staticmethod
    def sanitize(string: str) -> str:
        """Clean up a string.

        1. Strip non-alphanumerical characters
        2. Lowercase
        3. Replace all spaces by hyphens

        Parameters
        ----------
        string : str
            String to process.

        Returns
        -------
        : str
            Processed string.
        """
        return "".join(re.findall(r"[A-Za-z0-9 ]+", string)).lower().replace(" ", "-")

    def run(self, lines: typing.List[str]) -> typing.List[str]:
        r"""Overwritten method to process the input `Markdown` lines.

        Paramaters
        ----------
        lines : typing.List[str]
            `Markdown` content (split by `\n`).

        Returns
        -------
        : typing.List[str]
            Same list of lines, processed.
        """
        for i, line in enumerate(lines):
            for decl in re.findall(r"(%\[.+?\]\(.+?\))", line):
                id_, src = re.match(r"%\[(.*)\]\((.*)\)", decl).groups()
                id_ = self.sanitize(id_)

                lines[i] = line.replace(decl, self.html(id_, src))

        return lines


class ScriptExtension(Extension):
    """Extension to be imported when calling for the renderer."""

    def extendMarkdown(self, md: Markdown):
        """Overwritten method to process the content.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        Notes
        -----
        Since we are abusing the `Markdown` link syntax the preprocessor needs to be
        called with a high priority.
        """
        md.preprocessors.register(
            ScriptPreprocessor(md), name="script-tags", priority=100
        )
