# Module `markdown_script`

Python-Markdown extension processing the `%[]()` markers into `<script>` tags.

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

## Example:

```python
import markdown
provided = "%[Run script ?module](/src/script.js)"
rendered = markdown.markdown(provided, extensions=[ScriptExtension()])
expected = '<p id="run-script"><script src="/src/script.js" type="module"></script></p>'
assert rendered == expected
```

**Classes**

- [`ScriptPreprocessor`](#markdown_scriptscriptpreprocessor): Preprocessor to catch and
  replace the `%[]()` markers.
- [`ScriptExtension`](#markdown_scriptscriptextension): Extension proper, to be imported
  when calling for the `Markdown` renderer.

## Classes

### `markdown_script.ScriptPreprocessor`

Preprocessor to catch and replace the `%[]()` markers.

We are here abusing the `Markdown` link syntax; we need to run it *before* the regular
processing of the `Markdown` content.

**Methods**

- [`html()`](#markdown_scriptscriptpreprocessorhtml): Return the HTML block including
  the parameters.
- [`sanitize()`](#markdown_scriptscriptpreprocessorsanitize): Clean up a string intended
  as a HTML element `id`.
- [`run()`](#markdown_scriptscriptpreprocessorrun): Overwritten method to process the
  input `Markdown` lines.

#### Constructor

```python
ScriptPreprocessor(md: Markdown)
```

All methods except `run()` from `markdown.preprocessors.Preprocessor`.

**Parameters**

- `md` \[`markdown.core.Markdown`\]: Internal `Markdown` object to process.

#### Methods

##### `markdown_script.ScriptPreprocessor.html`

```python
html(id_: str, src: str, mod: bool = False) -> str:
```

Return the HTML block including the parameters.

Returned HTML:

```html
<p id=""><script src=""></script></p>
```

**Parameters**

- `id_` \[`str`\]: The `id` of the HTML elements. To be fetched via `.getElementById()`
  in the script itself.
- `src` \[`str`\]: The path to the script.
- `mod` \[`bool`\]: Whether the linked script is a `JavaScript` module.

**Returns**

- \[`str`\]: HTML tag with attributes.

**Decoration** via `@staticmethod`.

##### `markdown_script.ScriptPreprocessor.sanitize`

```python
sanitize(string: str) -> str:
```

Clean up a string intended as a HTML element `id`.

- Strip non-alphanumerical characters
- Lowercase
- Replace all spaces by hyphens

**Parameters**

- `string` \[`str`\]: String to process.

**Returns**

- \[`str`\]: Processed string.

**Decoration** via `@staticmethod`.

##### `markdown_script.ScriptPreprocessor.run`

```python
run(lines: list[str]) -> list[str]:
```

Overwritten method to process the input `Markdown` lines.

**Parameters**

- `lines` \[`list[str]`\]: `Markdown` content (split by `\n`).

**Returns**

- \[`list[str]`\]: Same list of lines, but processed (*e.g.*, containing HTML elements
  already).

### `markdown_script.ScriptExtension`

Extension proper, to be imported when calling for the `Markdown` renderer.

**Methods**

- [`extendMarkdown()`](#markdown_scriptscriptextensionextendmarkdown): Overwritten
  method to process the content.

#### Constructor

```python
ScriptExtension()
```

#### Methods

##### `markdown_script.ScriptExtension.extendMarkdown`

```python
extendMarkdown(md: Markdown) -> None:
```

Overwritten method to process the content.

**Parameters**

- `md` \[`markdown.core.Markdown`\]: Internal `Markdown` object to process.

**Notes**

Since we are abusing the `Markdown` link syntax the preprocessor needs to be called with
a high priority (100).
