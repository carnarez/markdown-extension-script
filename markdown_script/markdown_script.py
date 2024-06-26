"""Python-Markdown extension processing the `%[]()` markers into `<script>` tags.

`pip install git+https://github.com/carnarez/markdown-script` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

This was made to allow introducing fancier rendering (compared to static images) of
plots (for instance) in `Markdown`. **Use with caution**, only allow trusted/reviewed
`JavaScript` to run on your pages.

The **`type="module"`** attribute is made available via the `?module` keyword in the alt
text. This keyword is located in the alt text to avoid breaking common renderer
behaviour (GitHub included). It is expected to be separated from the actual alt text
(used as object `id`) by a space, and be the last content within the alt text provided
in between the square brackets (`[]`). (If unclear see example right below.)

Example:
-------
```python
import markdown
provided = "%[Run script ?module](/src/script.js)"
rendered = markdown.markdown(provided, extensions=[ScriptExtension()])
expected = '<p id="run-script"><script src="/src/script.js" type="module"></script></p>'
assert rendered == expected
```

"""

import re

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class ScriptPreprocessor(Preprocessor):
    """Preprocessor to catch and replace the `%[]()` markers.

    We are here abusing the `Markdown` link syntax; we need to run it *before* the
    regular processing of the `Markdown` content.
    """

    def __init__(self, md: Markdown) -> None:
        """All methods except `run()` from `markdown.preprocessors.Preprocessor`.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        """
        super().__init__(md)

    @staticmethod
    def html(id_: str, src: str, mod: bool = False) -> str:
        """Return the HTML block including the parameters.

        Returned HTML:

        ```html
        <p id=""><script src=""></script></p>
        ```

        Parameters
        ----------
        id_ : str
            The `id` of the HTML elements. To be fetched via `.getElementById()` in the
            script itself.
        src : str
            The path to the script.
        mod : bool
            Whether the linked script is a `JavaScript` module.

        Returns
        -------
        : str
            HTML tag with attributes.

        """
        return (
            f'<p id="{id_}"><script src="{src}" type="module"></script></p>'
            if mod
            else f'<p id="{id_}"><script src="{src}"></script></p>'
        )

    @staticmethod
    def sanitize(string: str) -> str:
        """Clean up a string intended as a HTML element `id`.

        * Strip non-alphanumerical characters
        * Lowercase
        * Replace all spaces by hyphens

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

    def run(self, lines: list[str]) -> list[str]:
        r"""Overwritten method to process the input `Markdown` lines.

        Parameters
        ----------
        lines : list[str]
            `Markdown` content (split by `\n`).

        Returns
        -------
        : list[str]
            Same list of lines, but processed (*e.g.*, containing HTML elements
            already).

        """
        escaped = 0

        for i, line in enumerate(lines):
            if line.startswith("```"):
                escaped = line.count("`")

            if escaped and line == escaped * "`":
                escaped = 0

            if not escaped:
                for m in re.finditer(r"%\[(.+?)\]\((.+?)\)", line):
                    id_, src = list(map(str.strip, m.groups()))

                    # check for a potential module marker
                    mod = False
                    if (m_ := re.search(r"(.*)\s+\?module$", id_)) is not None:
                        id_ = m_.group(1)
                        mod = True

                    id_ = self.sanitize(id_)

                    lines[i] = line.replace(m.group(0), self.html(id_, src, mod))

        return lines


class ScriptExtension(Extension):
    """Extension proper, to be imported when calling for the `Markdown` renderer."""

    def extendMarkdown(self, md: Markdown) -> None:
        """Overwritten method to process the content.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        Notes
        -----
        Since we are abusing the `Markdown` link syntax the preprocessor needs to be
        called with a high priority (100).

        """
        md.preprocessors.register(
            ScriptPreprocessor(md),
            name="script-tags",
            priority=100,
        )
