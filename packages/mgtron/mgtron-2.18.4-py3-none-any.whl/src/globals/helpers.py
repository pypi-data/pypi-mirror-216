"""Global helper functions for the application."""

import logging

from threading import Thread
from pathlib import Path

from dearpygui import dearpygui as dpg

loggi = logging.getLogger(name=__name__)

BLE_BTNS_LIST: set[str] = {
    "save button",
    "quick__load",
    "custom_save",
    "custom_load_button",
    "delete_button",
    "Alpha\nConfig",
    "Bravo\nConfig",
    "Charlie\nConfig",
    "Delta\nConfig",
    "Echo\nConfig",
    "Fox\nConfig",
    "mssn_scan_jam",
    217,
    210,
}

WIFI_BTNS_LIST: set[str] = {
    "save button",
    "quick__load",
    "custom_save",
    "custom_load_button",
    "delete_button",
    "Alpha\nConfig",
    "Bravo\nConfig",
    "Charlie\nConfig",
    "Delta\nConfig",
    "Echo\nConfig",
    "Fox\nConfig",
    "mssn_bluetooth_scan",
    217,  # Load button after being pressed
    210,  # Quick load button after being pressed
}

ROOT = Path(__file__).parent.parent.parent


def version_getter() -> str | None:
    """Get the latest version from the CHANGELOG file."""
    # Touch the file if it doesn't exist
    # pathlib.Path(ROOT / "CHANGELOG.md").touch()
    with open(
            ROOT / "src" / "assets" / "CHANGELOG.cpy", encoding="utf-8"
    ) as file:
        for line in file:
            if "##" in line and "YEAR MONTH DAY" not in line:
                correct_line = line.split("-")[0].strip()
                version = correct_line.split("[")[1]

                return version.strip("]")
        return None


__version__ = version_getter()


def disble_select_btns(*btns: list[str], _dpg: dpg):
    """Disable the buttons passed into the function."""
    loggi.debug(msg=f"{disble_select_btns.__name__}()")

    for btn in btns:
        try:
            _dpg.configure_item(item=btn, enabled=False)
            loggi.info(msg=f"Button {btn} disabled")

            loggi.debug("Buttons disabled")
        except SystemError as err:
            loggi.error("%s", err)
            loggi.error("Buttons not disabled")

    loggi.debug("%s() complete", disble_select_btns.__name__)


def enable_select_btns(*btns: list[str], _dpg: dpg):
    """Enable the buttons passed into the function."""
    loggi.debug(msg=f"{enable_select_btns.__name__}()")

    for btn in btns:
        try:
            _dpg.configure_item(item=btn, enabled=True)
            loggi.info(msg=f"Button {btn} enabled")

            loggi.debug("Buttons enabled")
        except SystemError as err:
            loggi.error("%s", err)
            loggi.error("Buttons not enabled")

    loggi.debug("%s() complete", enable_select_btns.__name__)


class ThreadWithReturnValue(Thread):
    """Create a thread that returns a value."""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs={}
                 ):
        """Initialize the thread."""
        Thread.__init__(
            self,
            group,
            target,
            name,
            args,
            kwargs
        )
        self._return = None

    def run(self):
        """Run the thread."""
        if self._target is not None:
            self._return = self._target(
                *self._args,
                **self._kwargs
            )

    def join(self, *args):
        """Join the thread."""
        Thread.join(self, *args)
        return self._return
