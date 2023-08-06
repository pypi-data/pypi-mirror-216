# Wideprint

[![PyPI - Version](https://img.shields.io/pypi/v/wideprint.svg)](https://pypi.org/project/wideprint)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wideprint.svg)](https://pypi.org/project/wideprint)

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install wideprint
```

## Usage

`def print_columns(data:Iterable, columns:int=3, sep:str=" ", alignment:Literal[">","<","^"]=">")`
 
 ```python
 from wideprint import print_columns
 
 print_columns(
    data      = ["aaaa","b","c","d","e","f","g","h","i","j","kkk","l","m","n","o"],
    columns   = 3,
    sep       = "  ",
    alignment = "<"
)
 ```

 ```text
aaaa  b    c
d     e    f
g     h    i
j     kkk  l
m     n    o
```
## License

`wideprint` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
