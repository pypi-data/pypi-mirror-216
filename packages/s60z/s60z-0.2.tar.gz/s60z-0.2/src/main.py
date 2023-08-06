""" The purpose of this program is to create a graphical user interface (GUI) using dearpygui, a python module, to simplify the Band Changing Process for the S60z software-defined radio (SDR). For this program to work, you need a specific

hardware configuration. To power the S60z, a 12V DC power source is required. The S60z should be accompanied by a sufficient power supply for use. This program works by integrating scripts present on both 

the SDR and the host computer. To work, all scripts required must be present on both devices. The S60z works on a yocto-based Linux operating system, and the host computer is expected to be operating on Arch 

Linux. A hard-wired ethernet connection between the host computer and the SDR is required for operational use. The wired subnet of the host computer must match that of the I.P. address of the SDR. The I.P. address 

of the SDR is a static IP address and can be found on a note located physically on the SDR. If the subnets do not match, it is not possible to execute commands via SSH (a secure shell network protocol), because

these two pieces of hardware will communicate solely over a network. Once the S60z hardware has been configured properly, and connected to the host computer with a correct wired I.P. address subnet, add the proper scripts

that can be located and found on both devices, you can run this script. Upon launch, the script will open a GUI on the host computer that will display interactive buttons with RF (radio frequency) information on them. The 

user will be able to then change the Band of the signal they are currently generating at the click of a button by remotely executing a range of commands from the host computer based on set parameters found in the script 

below. A Custom Input field for values is also currently in development. """


# Import the required modules and libraries.

from .gui.helpers import send_all
from .gui.helpers import close
from .gui.neighborhood_list import get_earfcn_values
import pathlib
import subprocess
import logging
import dearpygui.dearpygui as dpg


# Create the dpg window and subsequent context.


# Creation of Global Variables that will be used throughout the program.

ROOT = pathlib.Path(__file__).resolve().parent.parent
file = ROOT / "shell_scripts" / "localbandchange.sh"
ADJUSTMENT = 110
re_pos = 40
picture_file = ROOT / "images" / "ca_logo.png"


logger = logging.getLogger(name=__name__)
dpg.create_context()
# Create the button theme colors for the GUI buttons as well as the correct parameters for the Cell Antenna Logo.

with dpg.theme() as grn_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 55, 0, 255))  # GREEN

with dpg.theme() as red_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED

# Addition of the Cell Antenna Logo to the program

width, height, channels, data = dpg.load_image(f"{picture_file}")
with dpg.texture_registry(show=True):
    dpg.add_static_texture(
        width=width,
        height=height,
        default_value=data,
        tag="texture_tag"
    )

# Function of the table is listed in the definition.


def lookup_table(band_number: str) -> tuple[str, str, str, str]:
    """ Create A Lookup table that will use structured pattern matching in order to match the tag of a button 
    number and assign corresponding variable values that will be passed into a function. """
    logger.info(f"SENDER: {band_number}")

    match band_number:
        case 1:
            return (str(18300), str(300), str(1), str(20))
        case 2:
            return (str(18900), str(900), str(2), str(20))
        case 3:
            return (str(19575), str(1575), str(3), str(20))
        case 4:
            return (str(20175), str(2175), str(4), str(20))
        case 5:
            return (str(20525), str(2525), str(5), str(10))
        case 7:
            return (str(21100), str(3100), str(7), str(20))
        case 8:
            return (str(21625), str(3625), str(8), str(10))
        case 10:
            return (str(22450), str(4450), str(10), str(20))
        case 11:
            return (str(22850), str(4850), str(11), str(10))
        case 12:
            return (str(23095), str(5095), str(12), str(10))
        case 13:
            return (str(23230), str(5230), str(13), str(10))
        case 14:
            return (str(23300), str(5330), str(14), str(10))
        case 17:
            return (str(23790), str(5790), str(17), str(10))
        case 20:
            return (str(24300), str(6300), str(20), str(20))
        case 21:
            return (str(24525), str(6525), str(21), str(15))
        case 25:
            return (str(26365), str(8365), str(25), str(20))
        case 26:
            return (str(26865), str(8865), str(26), str(15))
        case 28:
            return (str(27435), str(9435), str(28), str(20))
        case 30:
            return (str(27710), str(9820), str(30), str(10))
        case 66:
            return (str(132322), str(66886), str(66), str(20))
        case 71:
            return (str(133297), str(68761), str(71), str(20))
        case _:
            logger.info(f"\nSENDER: {type(band_number)}\n")
            raise ValueError("Incorrect Band Number Passed")


# Creation of a function that takes in the button Tag as an input and based on that tag input, it matches it to the corresponding values required for that band number to properly display.
# That information is passed along to the subprocess command that runs commands in the terminal from python.

def my_function(sender):

    ULEARFCN, DLEARFCN, BAND, BAND_WIDTH = lookup_table(sender)
    command = f"{file} {ULEARFCN} {DLEARFCN} {BAND} {BAND_WIDTH}"

    print(subprocess.run([command
                          ], shell=True))

# Creation of the callback function that gets activated whenever a button is pressed .


def button_callback(sender, app_data, user_data):
    logger.info(f"\nSENDER: {sender}\n")
    my_function(int(sender))


# Creation of the Dear Py Gui Window
with dpg.window(label="SDR GUI", no_scrollbar=True, no_collapse=True, height=735, width=550, no_close=True, no_move=True, tag="SDR_GUI", no_resize=True) as window:

    # When creating items within the scope of the context
    # manager, they are automatically "parented" by the
    # container created in the initial call. So, "window"
    # will be the parent for all of these items.

    # Adds the cell antenna logo image.

    dpg.add_image("texture_tag", pos=(230, 25))

    # Uses a for loop and structured pattern matching to create the list of buttons on the left side.

    for i in range(14):
        match i:
            case 1:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 20 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 2:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 55 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 3:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 90 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 4:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 125 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 5:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 160 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 7:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 195 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 8:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 230 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 10:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 265 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 11:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 300 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 12:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 335 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 13:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    0, 370 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case _:
                continue

    # Uses a for loop and structured pattern matching to create the list of buttons on the right side.

    for i in range(14, 72):
        match i:
            case 14:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 20 + ADJUSTMENT), width=250,)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 17:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 55 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 20:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 90 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 21:
                dpg.add_button(label=f"Band {i} (15 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 125 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 25:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 160 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 26:
                dpg.add_button(label=f"Band {i} (15 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 195 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 28:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 230 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 30:
                dpg.add_button(label=f"Band {i} (10 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 265 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 66:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 300 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case 71:
                dpg.add_button(label=f"Band {i} (20 MHZ Bandwidth)", callback=button_callback, tag=f"{i}", pos=(
                    300, 335 + ADJUSTMENT), width=250)
                dpg.bind_item_theme(theme=grn_btn_theme, item=f"{i}")
            case _:
                continue

# Addition of Custom Input Field

    with dpg.child_window(pos=(5, 575 - re_pos), height=25, width=450, tag="Custom_Input_Fields", no_scrollbar=True, border=False):
        dpg.add_text(" ULEARFCN      DLEARFCN        BAND           B.W")
    with dpg.child_window(pos=(5, 550 - re_pos), height=25, width=300, tag="Custom_Input_Title", no_scrollbar=True, border=False):
        dpg.add_text("Enter in Your Custom Values Below:")
    with dpg.child_window(pos=(5, 625 - re_pos), height=25, width=550, tag="Custom_Freq_Input_Title", no_scrollbar=True, border=False):
        dpg.add_text("Enter a Frequency Value Below: Must be close to the Middle Freq. of the Band")
    with dpg.child_window(pos=(5, 675 - re_pos), height=40, width=550, no_scrollbar=True, border=False, tag="Display_EARFCN_Values"):
        dpg.add_text("The corresponding EARFCN values can be found below along with the Band Number.\nYou may input them into the Custom Values Field, along with your desired \nbandwidth.")

    dpg.add_input_text(tag="Single_Band_Input", pos=(0, 650 - re_pos), width=75, no_spaces=True)
    dpg.add_input_text(tag="ULEARFCN_VALUE", pos=(0, 600 - re_pos), width=75, no_spaces=True)
    dpg.add_input_text(tag="DLEARFCN_VALUE", pos=(100, 600 - re_pos), width=75, no_spaces=True)
    dpg.add_input_text(tag="BAND_VALUE", pos=(200, 600 - re_pos), width=75, no_spaces=True)
    dpg.add_input_text(tag="BW_VALUE", pos=(300, 600 - re_pos), width=75, no_spaces=True)

# Creation of Buttons used to send all the custom input parameters as well as the frequency converter

    dpg.add_button(label="Send All", callback=send_all, pos=(400, 600 - re_pos), tag="Send_All")
    dpg.bind_item_theme(theme=grn_btn_theme, item="Send_All")

    dpg.add_button(label="Send", callback=get_earfcn_values, pos=(100, 650 - re_pos), tag="send_band")
    dpg.bind_item_theme(theme=grn_btn_theme, item="send_band")

# Creation of the Popup Window that is initially hidden in the program

    with dpg.child_window(pos=(50, 367), show=False, tag="popup_window", height=150, width=450, no_scrollbar=True):
        dpg.add_text("        Error: You have entered an improper value! \n  This Value may not be in the range of supported frequencies. \n    The band numbers present on the Green Buttons display \n        the full range and capability of this device. \n   Your chosen frequency must fit within those bands, and \n should be a value close to the middle frequency of that band. \n       Or you have an invalid character in your input!\n       Or the value you entered is not a Whole Number!")
        dpg.add_button(show=True, tag="popup_window_button", height=25,
                       width=45, label="Close", callback=close, pos=(195, 120))
        dpg.bind_item_theme(theme=red_btn_theme, item="popup_window_button")


# The required DPG (dearpygui) commands to run and close the program

dpg.create_viewport(title='SDR GUI', width=550, height=735)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
