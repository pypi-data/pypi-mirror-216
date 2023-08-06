"""Top-level package for writio."""
import json
import logging
from pathlib import Path
import pandas as pd
import yaml


log = logging.getLogger(__name__)

__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.1"


def get_default_mode(path):
    if path.suffix == ".json":
        return "json"
    if path.suffix in [".yaml", ".yml"]:
        return "yaml"
    if path.suffix == ".csv":
        return "pandas-csv"
    if path.suffix == ".tsv":
        return "pandas-tsv"
    return "raw"


def dump(content, filename, mode=None, **kwargs):
    path = Path(filename)
    mode = mode or get_default_mode(path)
    if "pandas" in mode:
        if "index" not in kwargs:
            kwargs["index"] = False
        if isinstance(content, dict):
            content = pd.DataFrame.from_dict(content.values())
        if isinstance(content, list):
            content = pd.DataFrame.from_dict(content)
    else:
        if isinstance(content, pd.DataFrame):
            content = content.to_dict("records")
    with open(path, "w", encoding="utf-8") as f:
        if mode == "json":
            json.dump(content, f, ensure_ascii=False, indent=4)
        elif mode == "yaml":
            yaml.dump(content, f, allow_unicode=True, sort_keys=False)
        elif mode == "pandas-csv":
            content.to_csv(filename, **kwargs)
        elif mode == "pandas-tsv":
            content.to_csv(filename, sep="\t", **kwargs)
        elif mode == "raw":
            f.write(content)


def load(filename, mode=None, **kwargs):
    path = Path(filename)
    if not path.is_file():
        log.warning(f"{path} does not exist")
        return None
    mode = mode or get_default_mode(path)
    with open(path, "r", encoding="utf-8") as f:
        if mode == "json":
            return json.load(f)
        if mode == "yaml":
            return yaml.load(f, Loader=yaml.SafeLoader)
        if "pandas" in mode:
            if "keep_default_na" not in kwargs:
                kwargs["keep_default_na"] = False
            if "dtype" not in kwargs:
                kwargs["dtype"] = str
            if mode == "pandas-csv":
                return pd.read_csv(filename, **kwargs)
            if mode == "pandas-tsv":
                return pd.read_csv(filename, sep="\t", **kwargs)
        if mode == "csv2dict":
            res = pd.read_csv(filename, **kwargs)
            res = res.set_index(res.columns[0], drop=False)
            return {x.name: dict(x) for i, x in res.iterrows()}
        return f.read()
