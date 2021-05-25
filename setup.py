"""Make `pymdx-script` installable (via `pip install git+https://...`)."""

import setuptools

setuptools.setup(
    author="carnarez",
    description=(
        "Add support for <script> tags to Python-Markdown via the %[]() operator."
    ),
    install_requires=["markdown"],
    name="pymdx-script",
    py_modules=["pymdx_script"],
    url="https://github.com/carnarez/pymdx-script",
    version="0.0.1",
)
