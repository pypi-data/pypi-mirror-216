# cldf-ldd

CLDF schemata for language description and documentation.

![License](https://img.shields.io/github/license/fmatter/cldf-ldd)
[![PyPI](https://img.shields.io/pypi/v/cldf-ldd.svg)](https://pypi.org/project/cldf-ldd)
![Versions](https://img.shields.io/pypi/pyversions/cldf-ldd)

Details are found in [components](src/cldf_ldd/components).


* Adding components to a CLDF dataset:

```python
from cldf_ldd.components import StemTable
...
args.writer.cldf.add_component(StemTable)
...
args.writer.objects[StemTable["url"]].append({...})
```

* Adding [foreign keys](etc/foreignkeys.csv):

```python
from cldf_ldd import add_keys
...
add_keys(args.writer.cldf)
```

* Adding [additional columns](https://github.com/fmatter/cldf-ldd/blob/main/src/cldf_ldd/components/columns.json) to native tables:
```python
from cldf_ldd import add_columns
...
add_columns(args.writer.cldf)
```
