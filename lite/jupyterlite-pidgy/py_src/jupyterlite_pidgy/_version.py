import json
from pathlib import Path

__all__ = ["__version__", "__js__"]
__js__ = json.load(
    (Path(__file__).parent.resolve() / "labextension/package.json").read_bytes()
)
__version__ = __js__["version"]
