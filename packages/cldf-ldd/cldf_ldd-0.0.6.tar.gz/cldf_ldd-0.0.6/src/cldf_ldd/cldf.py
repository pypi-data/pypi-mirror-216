import yaml
from clldutils import jsonlib
from cldf_ldd.components import tables as components


try:
    from importlib.resources import files  # pragma: no cover
except ImportError:  # pragma: no cover
    from importlib_resources import files  # pragma: no cover

__all__ = ["keys", "columns", "components"]


cldf_path = files("cldf_ldd") / "components"

keys = yaml.load(open(cldf_path / "keys.yaml", "r"), Loader=yaml.SafeLoader)

columns = jsonlib.load(cldf_path / "columns.json")
