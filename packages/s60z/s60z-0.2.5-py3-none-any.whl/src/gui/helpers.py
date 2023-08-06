# Import the required modules and libraries.

import dearpygui.dearpygui as dpg
import subprocess
import re
import pathlib
import logging
from ..gui.scripts import get_ip_script_output


# Creation of the Global Path Variable used for many of the functions
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
file = ROOT / "shell_scripts" / "localbandchange.sh"
corrected_output = get_ip_script_output()

# Creation of the logging file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(name)s :: %(message)s :: %(levelname)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename=f"{ROOT}/s60z.log",
    filemode="w",
)

logger = logging.getLogger(name=__name__)


def send_all(sender, user_data, app_data):
    """Creation of the Send All function that sends the custom input values directly to the
    script that has been created to be executed on the SDR"""

    logger.info("Send All Button Pressed")
    values = [
        dpg.get_value("ULEARFCN_VALUE"),
        dpg.get_value("DLEARFCN_VALUE"),
        dpg.get_value("BAND_VALUE"),
        dpg.get_value("BW_VALUE")
    ]
    values_b = ''.join(str(values).split(','))
    values_c = ''.join(str(values_b).split("'"))
    values_d = values_c[1:-1]
    logger.info(values_d)
    if re.match("^[0-9 ]+$", values_d):
        logger.info("Valid Input for the 4 EARFCN Values.")
    else:
        logger.error("Invalid Input for the 4 EARFCN Values.")
        dpg.configure_item("popup_window", show=True)
    command = f"{file} {values_d} {corrected_output}"
    logger.info(command)
    subprocess.run([command], shell=True)


def close(sender, user_data, app_data):
    """ Creation of the button callback that calls the popup whenever an error is found 
    or a value error is raised. """

    logger.info("Popup and Item fields closed.")
    dpg.configure_item("popup_window", show=False)
    dpg.set_value(item="ULEARFCN_VALUE", value=" ")
    dpg.set_value(item="DLEARFCN_VALUE", value=" ")
    dpg.set_value(item="BW_VALUE", value=" ")
    dpg.set_value(item="Single_Band_Input", value=" ")
    dpg.set_value(item="BAND_VALUE", value=" ")
