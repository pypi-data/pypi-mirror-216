"""This module is used to scan for wifi signals and their frequencies."""

import time
import itertools
import logging
import subprocess
from pathlib import Path
from typing import Callable
from typing import Any

from colorama import Fore as F

from ..globals.helpers import ThreadWithReturnValue
from ..globals.helpers import enable_select_btns
from ..globals.helpers import WIFI_BTNS_LIST


loggey = logging.getLogger(__name__)

R = F.RESET
PATH = Path(__file__).parent.parent.parent


def find_signals_and_frequencies() -> subprocess.CompletedProcess:
    """Use the linux host to scan for wifi signals and frequencies."""
    loggey.debug(
        msg=f"Scanning for wifi signals and frequencies |"
        f" {find_signals_and_frequencies.__name__}"
    )

    output: subprocess.CompletedProcess = subprocess.run(
        [
            "nmcli",
            "-f",
            "SSID,BSSID,CHAN,FREQ,RATE,SIGNAL,SECURITY",
            "-t",
            "-e",
            "no",
            "dev",
            "wifi",
            "list",
            "--rescan",
            "yes",
        ],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )

    return output


def threaded_scan(
        _dpg,
        linux_data: subprocess.CompletedProcess
) -> subprocess.CompletedProcess:
    """Scan for wifi signals and frequencies in a thread."""

    try:
        linux_data = ThreadWithReturnValue(
            target=linux_data,
        )
        linux_data.start()

        _dpg.add_text(
            tag="scan_text",
            default_value="Scanning"
        )

        _dpg.add_text(
            tag="scan_text_",
            default_value='-' * 78
        )

        for i in range(1, 7):
            time.sleep(1)
            _dpg.configure_item(
                item="scan_text",
                default_value="Scanning" + "." * i
            )

        linux_data = linux_data.join()

        _dpg.delete_item(item="scan_text")
        _dpg.delete_item(item="scan_text_")
    except SystemError:
        loggey.error(msg="Wifi scan window not found")

        with _dpg.window(
            tag="wifi_scan_widow",
            no_scrollbar=True,
            no_collapse=True,
            no_resize=True,
            no_title_bar=True,
            no_move=True,
            modal=True,
            pos=(0, 0),
            width=880,
            height=735,
        ):
            _dpg.configure_item(item=12, show=False)

            _dpg.add_text(
                parent="wifi_scan_widow",
                pos=(
                    _dpg.get_item_width("wifi_scan_widow") / 2 - 50,
                    _dpg.get_item_height("wifi_scan_widow") / 2 - 50
                ),
                tag="scan_text",
                default_value="Scanning"
            )

        for i in range(1, 7):
            time.sleep(1)
            _dpg.configure_item(
                pos=(
                    _dpg.get_item_width("wifi_scan_widow") / 2 - 50,
                    _dpg.get_item_height("wifi_scan_widow") / 2 - 50
                ),
                item="scan_text",
                default_value="Scanning" + "." * i
            )

        linux_data = linux_data.join()
        _dpg.delete_item(item="wifi_scan_widow")
        enable_select_btns(*WIFI_BTNS_LIST, _dpg=_dpg)
        _dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=57,  # WTF.. Only hard coding the color works
        )

        try:
            _dpg.delete_item(item=12)
        except SystemError:
            loggey.warning(msg="Wifi scan window not found")

    return linux_data


def format_data(
        linux_data: Callable[[], subprocess.CompletedProcess],
        _dpg: Any,
) -> list[dict[str, str]]:
    """Format the data in the subprocess.CompletedProcess object."""
    loggey.debug(
        msg=f"Formatting data | {format_data.__name__}"
    )

    linux_data = threaded_scan(_dpg=_dpg, linux_data=linux_data)

    # Put each line of the output into its own list
    output_list: list[str] = [
        i for i in linux_data.stdout.split(sep="\n") if i != ""
    ]

    formatted_data: list[dict[str, str]] = []

    for data in output_list:
        ssid: str = data.split(sep=":")[0]
        bssid: list[str] = ":".join(
            data.split(sep=":")[1:7]
        )
        channel: str = data.split(sep=":")[7]
        frequency: str = data.split(sep=":")[8]
        rate: str = data.split(sep=":")[9]
        signal: str = data.split(sep=":")[10]
        security: str = data.split(sep=":")[11]

        formatted_data.append(
            {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "frequency": frequency,
                "rate": rate,
                "signal": signal,
                "security": security,
            }
        )

    return formatted_data


def freqs_and_sigs(
    formatted_data: dict[str, str],
    short_list: bool = False
) -> dict[int, float]:
    """Return a list of frequencies and signals."""
    # zip together the frequencies and signals and allow duplicates
    matched_sigs_and_freqs: dict[int, float] = {

        int(data["signal"]): float(data["frequency"].split(sep=" ")[0])
        for data in formatted_data
    }

    if short_list:
        # reduce the dictionary to the top 8 strongest signals
        top_eight = dict(itertools.islice(
            matched_sigs_and_freqs.items(),
            8
        ))

        # convert the itertools object to a dictionary
        top_eight = dict(enumerate(top_eight.values(), start=1))

        # if the dictionary is not eight items long, fill it with zeros
        if len(top_eight) != 8:
            for i in range(1, 9):
                if i not in top_eight.keys():
                    top_eight[i] = 0.0

            loggey.warning(
                msg=f"Dictionary was not eight items long |"
                f" {freqs_and_sigs.__name__}"
            )

    return matched_sigs_and_freqs if not short_list else top_eight


def main():
    """Run the module as a script."""
    data = format_data(find_signals_and_frequencies, _dpg=None)

    _ = [print(i) for i in data]


if __name__ == "__main__":
    main()
