from setuptools import setup

name = "types-Flask-Cors"
description = "Typing stubs for Flask-Cors"
long_description = '''
## Typing stubs for Flask-Cors

This is a PEP 561 type stub package for the `Flask-Cors` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Flask-Cors`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Flask-Cors. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `b8ab395d4bafd6352560e74b636744d49a9bcd6e` and was tested
with mypy 1.4.1, pyright 1.1.315, and
pytype 2023.6.2.
'''.lstrip()

setup(name=name,
      version="4.0.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-Cors.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Flask>=2.0.0'],
      packages=['flask_cors-stubs'],
      package_data={'flask_cors-stubs': ['__init__.pyi', 'core.pyi', 'decorator.pyi', 'extension.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
