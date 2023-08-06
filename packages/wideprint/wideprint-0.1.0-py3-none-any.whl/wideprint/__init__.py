"""
This module contains a single helper function to tabulate column names when you need to
review a dataset with many columns

```python
from wideprint import print_columns
```
"""

from typing import Iterable, Literal
def print_columns(data:Iterable, columns:int=3, sep:str=" ", alignment:Literal[">","<","^"]=">"):
    """Prints a list of objects in columns.
    
    `data` should be an iterable object, such as a list. Each element of data will be converted to a string using the built in `str()`
    `sep` is a string used to separate the columns. defaults to `' '`
    `alignment` is a string used to align the columns. It can take the values `">"`, `"<"`, or `"^"` which mean right align, left align, centre align respectively. defaults to `'>'`.

    Example:
    >>> print_columns(["aaaa","b","c","d","e","f","g","h","i","j","kkk","l","m","n","o"], 3, "  ", "<")
    aaaa  b    c
    d     e    f
    g     h    i
    j     kkk  l
    m     n    o
    """
    data = [*data]
    data += [""]*(len(data) - len(data)//columns*columns)
    column_data = []
    column_lengths = []
    for i in range(columns):
        column_data.append(
            new_column := list(map(str, data[i::columns])),
        )
        column_lengths.append(max(len(item) for item in new_column))
    
    

    datas, lengths = zip(*zip(column_data,column_lengths))
    outstring=[]
    for data in zip(*datas):
        fmt_string = sep.join(f"{{:{alignment}{length}}}" for length in lengths)
        outstring.append(fmt_string.format(*data))
    print("\n".join(outstring))