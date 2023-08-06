from setuptools import setup

name = "types-flake8-plugin-utils"
description = "Typing stubs for flake8-plugin-utils"
long_description = '''
## Typing stubs for flake8-plugin-utils

This is a PEP 561 type stub package for the `flake8-plugin-utils` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-plugin-utils`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-plugin-utils. All fixes for
types and metadata should be contributed there.

*Note:* The `flake8-plugin-utils` package includes type annotations or type stubs
since version 1.3.3. Please uninstall the `types-flake8-plugin-utils`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `d5f0d155d1d847d2aab3566ba196ff031d94a1bf` and was tested
with mypy 1.4.1, pyright 1.1.315, and
pytype 2023.6.2.
'''.lstrip()

setup(name=name,
      version="1.3.7.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-plugin-utils.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_plugin_utils-stubs'],
      package_data={'flake8_plugin_utils-stubs': ['__init__.pyi', 'plugin.pyi', 'utils/__init__.pyi', 'utils/assertions.pyi', 'utils/constants.pyi', 'utils/equiv_nodes.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
