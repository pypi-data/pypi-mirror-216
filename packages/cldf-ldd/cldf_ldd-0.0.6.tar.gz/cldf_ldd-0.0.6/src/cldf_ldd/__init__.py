"""Top-level package for cldf-ldd."""
import functools
import logging
import colorlog
from cldf_ldd.cldf import columns
from cldf_ldd.cldf import keys
from cldf_ldd.components import *


try:
    from importlib.resources import files  # pragma: no cover
except ImportError:  # pragma: no cover
    from importlib_resources import files  # pragma: no cover


log = logging.getLogger(__name__)


__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.6"


def valid_parts(name, dataset, table, column, row):
    value = row[column.name]
    if value and None in value:
        raise ValueError(f"None in {value} in column {column}")


validators = [
    (
        None,
        "http://cldf.clld.org/v1.0/terms.rdf#segments",
        functools.partial(valid_parts, "Segments"),
    ),
]


def add_columns(ds):
    for table in list(ds.components.keys()) + [str(x.url) for x in ds.tables]:
        if table in columns:
            ds.add_columns(table, *columns[table])


def validate(ds):
    ds.validate(validators=validators)


def add_keys(ds):
    cldf_tables = list(ds.components.keys()) + [
        str(x.url) for x in ds.tables
    ]  # a list of tables in the dataset
    for src, key1, goal, key2 in keys:
        if src in cldf_tables:
            if goal in cldf_tables:
                ds.add_foreign_key(src, key1, goal, key2)
            else:
                log.debug(
                    f"Table {src} has the foreign key {key1}, but there is no table {goal}."
                )
