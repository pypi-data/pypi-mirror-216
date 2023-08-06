import json
from contextlib import contextmanager
from pathlib import Path
from typing import Callable
from inspect import cleandoc

import docker


@contextmanager
def get_config(config_file: str):
    """
    Opens config file and returns parsed JSON object.
    """
    with open(config_file, "r") as f:
        yield json.load(f)
