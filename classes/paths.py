import os
import sys


def resource_path(relative_path):
    """Resolve a path to a bundled asset.

    Works both when running from source (path is relative to the project
    root) and when running as a PyInstaller-built .exe, where bundled data
    files are extracted to the temp folder in sys._MEIPASS instead.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
