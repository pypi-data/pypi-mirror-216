from .client import Client
from ._version import __version__
from ._dependencies import _try_optional_dependencies

OPTIONAL_DEPENDENCIES = _try_optional_dependencies()

def check_optional_dependencies():
    if not OPTIONAL_DEPENDENCIES:
        raise ImportError("Optional dependencies not found. Please install "
                          "ipywidgets and IPython to use the GUI.")

if OPTIONAL_DEPENDENCIES:
    from .gui.gui import gui_add_features
else:
    from .gui.gui import _ph_gui_add_features as gui_add_features

client = Client()
