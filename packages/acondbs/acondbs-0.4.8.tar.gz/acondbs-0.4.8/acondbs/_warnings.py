"""Configure the module warnings

https://docs.python.org/3/library/warnings.html

"""
import warnings
from pathlib import Path
from typing import Optional, Union

_module_path = Path(__file__).resolve().parent.parent
# the path to the dir in which the module is installed,
# i.e., the one dir above the module path.


def format(
    message: Union[Warning, str],
    category: type[Warning],
    filename: str,
    lineno: int,
    line: Optional[str] = None,
) -> str:
    try:
        filename = str(Path(filename).resolve().relative_to(_module_path))
    except Exception:
        pass
    ret = "{}:{}: {}\n".format(filename, lineno, message)
    return ret


warnings.formatwarning = format
