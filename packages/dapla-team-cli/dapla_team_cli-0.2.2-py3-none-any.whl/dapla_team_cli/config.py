"""CLI-wide config variables."""
import os
from pathlib import Path
from sys import platform

from rich.console import Console
from rich.style import Style


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "error": Style(color="red", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def get_config_folder_path(tmp: bool = False) -> str:
    """Gets the config folder path on current machine.

    Args:
        tmp: A true/false flag that determines whether function should return temporary folder or base folder.

    Raises:
        Exception: If the platform is not linux, darwin (macos) or windows.

    Returns:
        The config folder path, or temporary folder path inside config folder.
    """
    if platform in ("linux", "darwin"):
        config_folder_path = Path.home() / ".config/dapla-team-cli"
    elif platform == "win32":
        username = os.getlogin()
        config_folder_path = Path(rf"C:\Users\{username}\AppData\dapla-team-cli")
    else:
        raise RuntimeError("Unknown platform. The CLI only supports Unix and Windows based platforms.")

    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)

    if tmp:
        return str(config_folder_path / "tmp/")

    return str(config_folder_path)


try:
    __IPYTHON__  # type: ignore [name-defined]
    in_ipython_session = True
except NameError:
    in_ipython_session = False

DAPLA_TEAM_API_BASE = os.getenv("DAPLA_TEAM_API_BASE_URL", "https://team-api.dapla-staging.ssb.no")
