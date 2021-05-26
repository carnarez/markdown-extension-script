# Module `markdown_script`

Python-Markdown extension processing the `%[]()` markers into `<script>` tags.

`pip install git+https://github.com/carnarez/pymdx-script` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

This was made to allow introducing fancier rendering (compared to static images) of
plots (for instance) in `Markdown`. **Use with caution**, only allow trusted/reviewed
`JavaScript` to run on your pages.

**Example:**

```python
import markdown
provided = "%[Run script (d3.js)](/wherever/script.js)"
rendered = markdown.markdown(provided, extensions=[ScriptExtension()])
expected = '<p id="run-script-d3js"><script src="/wherever/script.js"></script></p>'
assert rendered == expected
```

**Classes:**

* [`ScriptPreprocessor`](#markdown_scriptscriptpreprocessor)
* [`ScriptExtension`](#markdown_scriptscriptextension)

## Classes

### `markdown_script.ScriptPreprocessor`

Preprocessor to catch and replace the `%[]()` markers.

We are here abusing the `Markdown` link syntax; we need to run it *before* the
regular processing of the `Markdown` content.

**Methods:**

* [`html()`](#markdown_scriptscriptpreprocessorhtml)
* [`sanitize()`](#markdown_scriptscriptpreprocessorsanitize)
* [`run()`](#markdown_scriptscriptpreprocessorrun)

#### Constructor

```python
ScriptPreprocessor(md: Markdown)
```

All methods except `run()` from `markdown.preprocessors.Preprocessor`.

**Parameters:**

* `md` [`markdown.core.Markdown`]: Internal `Markdown` object to process.

#### Methods

##### `markdown_script.ScriptPreprocessor.html`

```python
html(id_: str, src: str) -> str:
```

Return the HTML block including the parameters.

Returned HTML:

```html
<p id=""><script src=""></script></p>
```

**Parameters:**

* `id_` [`str`]: The `id` of the HTML elements. To be fetched via `.getElementById()` in the
    script itself.
* `src` [`str`]: The path to the script.

**Returns:**

* [`str`]: HTML tag with attributes.

**Decoration** via `@staticmethod`.

##### `markdown_script.ScriptPreprocessor.sanitize`

```python
sanitize(string: str) -> str:
```

Clean up a string intended as a HTML element `id`.

* Strip non-alphanumerical characters
* Lowercase
* Replace all spaces by hyphens

**Parameters:**

* `string` [`str`]: String to process.

**Returns:**

* [`str`]: Processed string.

**Decoration** via `@staticmethod`.

##### `markdown_script.ScriptPreprocessor.run`

```python
run(lines: typing.List[str]) -> typing.List[str]:
```

Overwritten method to process the input `Markdown` lines.

**Paramaters:**

* `lines` [`typing.List[str]`]: `Markdown` content (split by `\n`).

**Returns:**

* [`typing.List[str]`]: Same list of lines, but processed (*e.g.*, containing HTML elements
    already).

### `markdown_script.ScriptExtension`

Extension proper, to be imported when calling for the `Markdown` renderer.

**Methods:**

* [`extendMarkdown()`](#markdown_scriptscriptextensionextendmarkdown)

#### Constructor

```python
ScriptExtension()
```

#### Methods

##### `markdown_script.ScriptExtension.extendMarkdown`

```python
extendMarkdown(md: Markdown):
```

Overwritten method to process the content.

**Parameters:**

* `md` [`markdown.core.Markdown`]: Internal `Markdown` object to process.

**Notes:**

Since we are abusing the `Markdown` link syntax the preprocessor needs to be
called with a high priority (100).
