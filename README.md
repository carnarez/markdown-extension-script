# Module `pymdx_script`

Python-Markdown extension converting the `%[]()` markers into `<script>` tags.

Refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

**Example:**

```python
import markdown
provided = "%[Run script.js (d3.js)](/wherever/script.js)"
rendered = markdown.markdown(src, extensions=[ScriptExtension()])
expected = '<p id="run-scriptjs-d3js"><script src="/wherever/script.js"></script></p>'
assert rendered == expected
```

**Classes:**

- [`ScriptPreprocessor`](#pymdx_scriptscriptpreprocessor)
- [`ScriptExtension`](#pymdx_scriptscriptextension)

## Classes

### `pymdx_script.ScriptPreprocessor`

Preprocessor to catch and replace the `%[]()` markers.

**Methods:**

- [`html()`](#pymdx_scriptscriptpreprocessorhtml)
- [`sanitize()`](#pymdx_scriptscriptpreprocessorsanitize)
- [`run()`](#pymdx_scriptscriptpreprocessorrun)

#### Constructor

```python
ScriptPreprocessor(md: Markdown)
```

## Parameters

- `md` \[`markdown.core.Markdown`\]: `markdown.core.Markdown` object to process.

#### Methods

##### `pymdx_script.ScriptPreprocessor.html`

```python
html(id_: str, src: str) -> str:
```

Return the HTML block including the parameters.

**Parameters:**

- `id_` \[`str`\]: The `id` of the HTML elements.
- `src` \[`str`\]: The path to the script.

**Returns:**

- \[`str`\]: HTML elements.

**Decoration** via `@staticmethod`.

##### `pymdx_script.ScriptPreprocessor.sanitize`

```python
sanitize(string: str) -> str:
```

Clean up a string.

Strip a string from non-alphanumerical characters, lower case it, and replace all spaces
by hyphens.

**Parameters:**

- `string` \[`str`\]: String to process.

**Returns:**

- \[`str`\]: Processed string.

**Decoration** via `@staticmethod`.

##### `pymdx_script.ScriptPreprocessor.run`

```python
run(self, lines: typing.List[str]) -> typing.List[str]:
```

Overwritten method to process the input `Markdown` (split by `\n`).

**Paramaters:**

- `lines` \[`typing.List[str]`\]: `Markdown` content (split by `\n`).

**Returns:**

- \[`typing.List[str]`\]: Same list of lines, processed.

### `pymdx_script.ScriptExtension`

Extension proper.

**Methods:**

- [`extendMarkdown()`](#pymdx_scriptscriptextensionextendmarkdown)

#### Constructor

```python
ScriptExtension()
```

#### Methods

##### `pymdx_script.ScriptExtension.extendMarkdown`

```python
extendMarkdown(self, md: Markdown):
```

Overwritten method to process the content.

**Parameters:**

- `md` \[`markdown.core.Markdown`\]: `markdown.core.Markdown` object to process.

**Notes:**

Since we are abusing the `Markdown` link syntax the preprocessor needs to be called with
a high priority.
