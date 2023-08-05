"""Server extension for JupyterLab."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from ._version import __version__  # noqa
from .handlers.announcements import (  # noqa
    CheckForUpdate,
    CheckForUpdateABC,
    NeverCheckForUpdate,
)
from .serverextension import load_jupyter_server_extension  # noqa


def _jupyter_server_extension_paths():
    return [{"module": "jupyterlab"}]


def _jupyter_server_extension_points():
    from .labapp import LabApp

    return [{"module": "jupyterlab", "app": LabApp}]
