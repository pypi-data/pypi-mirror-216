from setuptools import setup

name = "types-annoy"
description = "Typing stubs for annoy"
long_description = '''
## Typing stubs for annoy

This is a PEP 561 type stub package for the `annoy` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`annoy`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/annoy. All fixes for
types and metadata should be contributed there.

*Note:* The `annoy` package includes type annotations or type stubs
since version 1.17.1. Please uninstall the `types-annoy`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `201940cdc12e61e3bf5bc3ee4c5fd71bcc23fdf9` and was tested
with mypy 1.4.1, pyright 1.1.316, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="1.17.8.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/annoy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['annoy-stubs'],
      package_data={'annoy-stubs': ['__init__.pyi', 'annoylib.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
