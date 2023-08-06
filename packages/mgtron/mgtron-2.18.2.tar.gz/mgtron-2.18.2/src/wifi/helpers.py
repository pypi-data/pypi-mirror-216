"""Helper functions for wifi business of the GUI."""

import logging
import random
from typing import Callable
from datetime import datetime

import dearpygui.dearpygui as dpg

from colorama import Fore as F

from ..gui.helpers import callstack_helper

from .scanning import find_signals_and_frequencies
from .scanning import format_data
from .scanning import freqs_and_sigs

from ..globals.helpers import disble_select_btns
from ..globals.helpers import enable_select_btns
from ..globals.helpers import WIFI_BTNS_LIST


loggei = logging.getLogger(name=__name__)

R = F.RESET


# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE
# Grey Button Theme
with dpg.theme() as grey_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 128, 128, 255))  # GREY


def wifi_scan_jam(sender) -> None:
    """Scan the local wifi channels and jam them."""
    loggei.info(msg="Scan jammer method called")

    disble_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)
    #  Determine if the scan is in progress; toggle button
    if dpg.get_item_theme(item=sender) == orng_btn_theme:
        dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=57,  # WTF.. Only hard coding the color works
        )
        loggei.debug(msg="WiFi scan button disabled")

        # Delete the open WiFi scan window
        dpg.delete_item(item=12)
        loggei.debug(msg="WiFi scan window deleted")
        enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)

    else:

        # Launch the window that will show the wifi information
        dpg.bind_item_theme(
            item=sender,
            theme=orng_btn_theme,
        )

        loggei.debug(msg="WIFI scan button enabled")

        with dpg.window(
            tag=12,
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
            with dpg.child_window(
                tag="ble_labels",
                pos=(0, 0),
                width=880,
                height=715,
            ):
                dpg.add_text(
                    default_value=" " * 2 + "SSID" + " " * 5 + "|" + " " * 2 +
                    "MAC" + " " * 1 + "|" + " " +
                    " " * 2 + "CHANNEL" + " " * 2 + "|" + " " * 2 +
                    "FREQ" + " " * 2 + "|" + " " * 2 + "RSSI"
                    + " " * 2 + "|" + " " * 2 + "BANDWIDTH" + " " * 2 + "|" +
                    " " * 2 + "SECURITY"
                    + " " * 2 + "|" + " " * 2 + "DATE" + " " * 2,
                    label="WIFI LIST",
                )
                dpg.add_text(
                    default_value='-'*89
                )

            with dpg.child_window(
                tag="wifi_list",
                no_scrollbar=True,
                pos=(0, 60),
                width=880,
                height=680,
            ):

                # Get the WiFi dict information and print to GUI
                all_data: list[dict[str, str]] = format_data(
                    find_signals_and_frequencies,
                    _dpg=dpg,
                )

                # [print(i) for i in all_data]

                for i, data in enumerate(all_data, start=1):

                    try:
                        # SSID | MAC | CHANNEL | FREQ | RSSI | BANDWIDTH |
                        # SECURITY | DATE
                        print_to_user = f"{i}. "\
                            f"{data.get('ssid')}"\
                            f"{' '* (1 if i > 9 else 2)}|"\
                            f"{' '* (1 if i > 9 else 1)}"\
                            f"{data.get('bssid')}"\
                            f"{' '* (14 - len(data.get('bssid')) + 1) if i > 9 else ' ' * (15 - len(data.get('bssid')))}|"\
                            f" {data.get('channel')}  | "\
                            f"  {data.get('frequency')}  | "\
                            f" {data.get('signal')}  | "\
                            f" {data.get('rate')}  | "\
                            f" {data.get('security')}  | "\
                            f" {datetime.now().strftime('%H:%M:%S')}"
                    except TypeError:
                        print_to_user = f"{i}. "\
                            "NO CONNECTION ESTABLISHED"

                    loggei.info(data)

                    dpg.add_button(
                        tag=f"wifi_result_{i}",
                        label=print_to_user,
                        callback=activate_wifi_algo,
                        user_data=data,
                        width=880,
                        height=40,
                    )

                    # dpg.add_text(
                    # default_value=print_to_user
                    # )
                    dpg.add_text(
                        tag=f"wifi_result_{i}_line",
                        default_value='-' * 89
                    )

                dpg.configure_item(
                    item=12,
                    modal=False,
                )
        loggei.debug(msg="Scan jammer method finished")


def activate_wifi_algo(sender, app_data, user_data: dict[str, str]) -> None:
    """Send all the requisite information to the MGTron board."""
    loggei.debug(msg=f"{activate_wifi_algo.__name__} called")

    loggei.info("User data: %s", user_data)
    loggei.info("App data: %s", app_data)
    loggei.info("Sender: %s", sender)

    freq = float(user_data.get('frequency').split(' ')[0])
    # print(f"{F.YELLOW}Frequency{R}: {freq}\n")

    channel_list: list[int] = discern_avail_channels(dpg)

    loggei.info("Channel list: %s", channel_list)

    # If there are no channels available, then all available
    if not channel_list:
        channel_list: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

    # print(f"{F.GREEN}Channel list{R}: {channel_list}\n")

    # randomly select a channel from the list
    channel = random.choice(list(channel_list))

    # print(f"{F.YELLOW}Channel{R}: {channel}\n")

    dpg.set_value(
        item=f"freq_{channel}",
        value=freq if isinstance(
            freq, float
        ) else 50.0
    )
    dpg.set_value(
        item=f"power_{channel}",
        value=100 if int(freq) != 50 else 0
    )
    dpg.set_value(
        item=f"bandwidth_{channel}",
        value=10 if int(freq) != 50 else 0
    )
    loggei.info(
        "Frequency, in sig strength order, discovered: %s", channel
    )

    # Automatically send the command to the MGTron board
    callstack_helper(channel=channel)


def wifi_kill_all(callstack_helper: Callable[[int, ], None]) -> None:
    """Insert and auto send the top eight scanned channels."""
    loggei.info(msg="Scan jammer method called")

    # dpg.configure_item(item=sender, label="SCANNING...")
    # dpg.bind_item_theme(item=sender, theme=red_btn_theme)  # type: ignore

    loggei.info(msg="SCANNING...")

    data = format_data(find_signals_and_frequencies, _dpg=dpg)

    freq_and_strength: dict[int, float] = freqs_and_sigs(data, short_list=True)

    loggei.warning(msg=f"Freq & Strength sorted: {freq_and_strength}")

    # print(f"{F.YELLOW}Freq & Strength sorted{R}: {freq_and_strength}\n")

    _ = [
        (
            dpg.set_value(
                item=f"freq_{i}", value=float(freq) if isinstance(
                    freq, float
                ) else 50.0
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=100 if int(freq) != 50 else 0),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=10 if int(freq) != 50 else 0),
            loggei.debug(  # type: ignore
                msg=f"Frequency, in sig strength order, discovered: {freq}"
            ),
            # Automatically send the command to the MGTron board
            callstack_helper(channel=i)
        )
        for i, freq in enumerate(freq_and_strength.values(), start=1)
    ]

    # # Stop looping scan jam if 'KILL ALL' is pressed and hovered over
    # if dpg.is_item_focused(test
    #         item="Stop_all_channels"):

    loggei.debug(msg="Scan jammer method finished")


def discern_avail_channels(_dpg: dpg) -> list[int]:
    """Determine which channel is available and return the channel number."""
    loggei.debug(msg=f"{discern_avail_channels.__name__} called")

    # Get all of the indicator colors
    indicator_color: list = [
        _dpg.get_item_theme(item=f"stats_{i}") for i in range(1, 9)
    ]

    loggei.info("Indicator color: %s", indicator_color)

    grey_theme = 30
    # Find out what channel numbers are available
    free_channels = indicator_color.count(grey_theme)

    loggei.info("Free channels: %s", free_channels)

    if not free_channels:
        loggei.warning(msg="No wifi channels available")
        return []

    # Transform all grey indicies to True and the rest to False
    indicator_color = [
        color == grey_theme for color in indicator_color
    ]

    loggei.info("Indicator color: %s", indicator_color)

    # Keep track of the indices as the channel numbers to the new list
    channel_numbers = [
        i for i, color in enumerate(indicator_color, start=1) if color
    ]

    loggei.info("Channel numbers returned: %s", channel_numbers)

    return channel_numbers
