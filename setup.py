"""Make `markdown-script` installable (via `pip install git+https://...`)."""

import setuptools  # type: ignore

setuptools.setup(
    author="carnarez",
    description=(
        "Add support for <script> tags to Python-Markdown via the %[]() operator."
    ),
    install_requires=["markdown"],
    name="markdown-script",
    package_data={"": ["*.pyi"]},
    py_modules=["markdown_script"],
    url="https://github.com/carnarez/markdown-script",
    version="0.0.1",
)
