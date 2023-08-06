# Import the required modules and libraries.

from colorama import Fore as F
import dearpygui.dearpygui as dpg
import logging
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
logging.info(ROOT)
R = F.RESET

logger = logging.getLogger(name=__name__)

""" Creation of the class that is used to forumlate the blueprint for every funciton
that involves the use or calculation of integral RF Values"""


class E_UTRA:
    """Table 5.7.3-1 E-UTRA channel numbers Downlink Only"""

    TABLE: dict[str, tuple[float, int]] = {
        # Band: (FDL_low, NOffs_DL)
        "1": (2110, 0),
        "2": (1930, 600),
        "3": (1805, 1200),
        "4": (2110, 1950),
        "5": (869, 2400),
        "6": (875, 2650),
        "7": (2620, 2750),
        "8": (925, 3450),
        "9": (1845, 3800),
        "10": (2110, 4150),
        "11": (1476, 4750),
        "12": (729, 5010),
        "13": (746, 5180),
        "14": (758, 5280),
        "17": (734, 5730),
        "18": (860, 5850),
        "19": (875, 6000),
        "20": (791, 6150),
        "21": (1496, 6450),
        "24": (1525, 7700),
        "25": (1900, 8040),
        "26": (859, 8690),
        "27": (852, 9040),
        "28": (758, 9210),
        "29": (717, 9660),
        "30": (2350, 9770),
        "31": (463, 9870),
        "32": (1900, 9920),
        "33": (1900, 36000),
        "34": (2010, 36200),
        "35": (1850, 36350),
        "36": (1930, 36950),
        "37": (1910, 37550),
        "38": (2570, 37750),
        "39": (1880, 38250),
        "40": (2300, 38650),
        "41": (2496, 39650),
        "42": (3400, 41590),
        "43": (3600, 43590),
        "44": (3700, 45590),
        "66": (2100, 66436),
        "71": (617, 68586),
    }

    # Creation of a second E_UTRA table that displays EARFCN UL Values

    TABLE2: dict[str, tuple[float, int]] = {
        # Band: (FUL_low, NOffs_UL)
        "1": (1920, 18000),
        "2": (1850, 18600),
        "3": (1710, 19200),
        "4": (1710, 19950),
        "5": (824, 20400),
        "6": (830, 20650),
        "7": (2500, 20750),
        "8": (880, 3450),
        "9": (1749.9, 21800),
        "10": (1710, 22150),
        "11": (1427.9, 22750),
        "12": (699, 23010),
        "13": (777, 23180),
        "14": (788, 23280),
        "17": (704, 23730),
        "18": (815, 23850),
        "19": (830, 24000),
        "20": (832, 24150),
        "21": (1447.9, 24450),
        "24": (1626.5, 25700),
        "25": (1850, 26040),
        "26": (814, 26690),
        "27": (807, 27040),
        "28": (703, 27210),
        #  "29": (717, 9660), # DOWNLINK ONLY
        "30": (2305, 27660),
        "31": (452.5, 27760),
        #   "32": (1900, 9920), # DOWNLINK ONLY
        "33": (1900, 36000),
        "34": (2010, 36200),
        "35": (1850, 36350),
        "36": (1930, 36950),
        "37": (1910, 37550),
        "38": (2570, 37750),
        "39": (1880, 38250),
        "40": (2300, 38650),
        "41": (2496, 39650),
        "42": (3400, 41590),
        "43": (3600, 43590),
        "44": (703, 45590),
        "66": (1710, 131972),
        "71": (663, 133122),
    }

    """ List of Bands that function in the U.S. Not used in the scope of this program but provides useful information and context """

    US_BANDS = [
        2,
        4,
        5,
        10,
        12,
        13,
        14,
        25,
        26,
        30,
        41,
        66,
        71,
    ]  # US bands we want to use

    @classmethod
    def _band_ranges(self) -> dict[list[int]]:
        """Define the ranges of earfcns for each band"""

        band_1 = [i for i in range(0, 600)]
        band_2 = [i for i in range(600, 1200)]
        band_3 = [i for i in range(1200, 1950)]
        band_4 = [i for i in range(1950, 2400)]
        band_5 = [i for i in range(2400, 2650)]
        band_6 = [i for i in range(2650, 2750)]
        band_7 = [i for i in range(2750, 3450)]
        band_8 = [i for i in range(3450, 3800)]
        band_9 = [i for i in range(3800, 4150)]
        band_10 = [i for i in range(4150, 4750)]
        band_11 = [i for i in range(4750, 4950)]
        band_12 = [i for i in range(5010, 5180)]
        band_13 = [i for i in range(5180, 5280)]
        band_14 = [i for i in range(5280, 5380)]
        band_17 = [i for i in range(5730, 5850)]
        band_18 = [i for i in range(5850, 6000)]
        band_19 = [i for i in range(6000, 6150)]
        band_20 = [i for i in range(6150, 6450)]
        band_21 = [i for i in range(6450, 6600)]
        band_24 = [i for i in range(7700, 8040)]
        band_25 = [i for i in range(8040, 8690)]
        band_26 = [i for i in range(8690, 9040)]
        band_27 = [i for i in range(9040, 9210)]
        band_28 = [i for i in range(9210, 9660)]
        band_29 = [i for i in range(9660, 9770)]  # Downlink only
        band_30 = [i for i in range(9770, 9870)]
        band_31 = [i for i in range(9870, 9920)]
        band_32 = [i for i in range(9920, 10360)]  # Downlink only
        band_33 = [i for i in range(36000, 36200)]
        band_34 = [i for i in range(36200, 36350)]
        band_35 = [i for i in range(36350, 36950)]
        band_36 = [i for i in range(36950, 37550)]
        band_37 = [i for i in range(37550, 37750)]
        band_38 = [i for i in range(37750, 38250)]
        band_39 = [i for i in range(38250, 38650)]
        band_40 = [i for i in range(38650, 39650)]
        band_41 = [i for i in range(39650, 41590)]
        band_42 = [i for i in range(41590, 43590)]
        band_43 = [i for i in range(43590, 45590)]
        band_44 = [i for i in range(45590, 46590)]
        band_66 = [i for i in range(66436, 67336)]
        band_71 = [i for i in range(68586, 68936)]

        return {
            "1": band_1,
            "2": band_2,
            "3": band_3,
            "4": band_4,
            "5": band_5,
            "6": band_6,
            "7": band_7,
            "8": band_8,
            "9": band_9,
            "10": band_10,
            "11": band_11,
            "12": band_12,
            "13": band_13,
            "14": band_14,
            "17": band_17,
            "18": band_18,
            "19": band_19,
            "20": band_20,
            "21": band_21,
            "24": band_24,
            "25": band_25,
            "26": band_26,
            "27": band_27,
            "28": band_28,
            "29": band_29,
            "30": band_30,
            "31": band_31,
            "32": band_32,
            "33": band_33,
            "34": band_34,
            "35": band_35,
            "36": band_36,
            "37": band_37,
            "38": band_38,
            "39": band_39,
            "40": band_40,
            "41": band_41,
            "42": band_42,
            "43": band_43,
            "44": band_44,
            "66": band_66,
            "71": band_71,
        }

    @classmethod
    def convert_to_frequency(cls, earfcn: list[int]) -> float | None:
        """Convert the earfcn to a center band frequency"""

        for band in E_UTRA._band_ranges().items():
            # print(band[1])
            for i in band[1]:
                try:
                    if int(i) == earfcn:
                        FDL_low, NOffs_DL = (
                            cls.TABLE.get(band[0])[0],
                            cls.TABLE.get(band[0])[1],
                        )
                        return FDL_low + 0.1 * (earfcn - NOffs_DL)
                    else:
                        print(f"{F.RED}Earfcn not found{R}")
                        return None
                except TypeError:
                    print("No band found for earfcn: {}".format(earfcn))
                    return None

    @classmethod
    def freq_to_dlearfcn(cls, freq: str) -> float | None:
        """Convert a frequency value to a downlink earfcn value (NDL)"""
        logger.info("freq_to_dlearfcn function has been called")

        for band in E_UTRA._band_ranges().items():
            logger.info(band[1])
            for i in band[1]:
                try:
                    if int(i) == freq:
                        FDL_low, NOffs_DL = (
                            cls.TABLE.get(band[0])[0],
                            cls.TABLE.get(band[0])[1],
                        )
                        return (freq - FDL_low) / 0.1 + NOffs_DL
                    else:
                        logger.error("Invalid Frequency Value")
                        return None
                except TypeError:
                    logger.error("No value found for frequency".format(freq))
                    return None

    """ Creation of a classmethod that serves as a lookup table that matches user input of a Frequency to a corresponding Band if it fits in the range. """

    @classmethod
    def lookup_table(self, freq: str) -> float:
        logger.info("Lookup Table function is in use")
        try:
            if float(freq) in range(2110, 2156):
                logger.info("this is band 4")
                return "4"
            elif float(freq) in range(2110, 2171):
                logger.info("this is band 10")
                return "10"
            elif float(freq) in range(2110, 2171):
                logger.info("this is band 1")
                return "1"
            elif float(freq) in range(2110, 2201):
                logger.info("this is band 66")
                return "66"
            elif float(freq) in range(1930, 1991):
                logger.info("this is band 2")
                return "2"
            elif float(freq) in range(1930, 1996):
                logger.info("this is band 25")
                return "25"
            elif float(freq) in range(1805, 1881):
                logger.info("this is band 3")
                return "3"
            elif float(freq) in range(925, 960):
                logger.info("this is band 8")
                return "8"
            elif float(freq) in range(869, 895):
                logger.info("this is band 5")
                return "5"
            elif float(freq) in range(859, 895):
                logger.info("this is band 26")
                return "26"
            elif float(freq) in range(2620, 2691):
                logger.info("this is band 7")
                return "7"
            elif float(freq) in range(1475, 1498):
                logger.info("this is band 11")
                return "11"
            elif float(freq) in range(734, 747):
                logger.info("this is band 17")
                return "17"
            elif float(freq) in range(729, 747):
                logger.info("this is band 12")
                return "12"
            elif float(freq) in range(746, 756):
                logger.info("this is band 13")
                return "13"
            elif float(freq) in range(758, 769):
                logger.info("this is band 14")
                return "14"
            elif float(freq) in range(758, 804):
                logger.info("this is band 28")
                return "28"
            elif float(freq) in range(791, 822):
                logger.info("this is band 20")
                return "20"
            elif float(freq) in range(1496, 1513):
                logger.info("this is band 21")
                return "21"
            elif float(freq) in range(2350, 2361):
                logger.info("this is band 30")
                return "30"
            elif float(freq) in range(617, 653):
                logger.info("this is band 71")
                return "71"
            else:
                logger.error(" Incorrect value")
        except ValueError:
            logger.error("Popup window triggered")
            dpg.configure_item(item="popup_window", show=True)

    """ Creation of the classmethod that is used to later convert a string to a list for later implementation with spaces being the delimitter. """

    @classmethod
    def change_to_string(self, string):
        logger.info("Conversion to string function is in use")
        li = list(string.split(' '))
        return li


""" Creation of the function that is used to convert a single frequency value to the corresponding EARFCN Values. There are two special cases with bands 71 and 66,
because the math required to get their uplink earfcns is differnt compared to the first 30 bands (majority of which are able to be used with the SDR). Thus if the returned
band value is 66 or 71, the two patterns are triggered and the subsequent code is executed. A default case remains for the return values for all the other bands that
do not require a special case in order to compute the correct corresponding EARFCN values"""


def get_earfcn_values(app_data, sender, user_data):
    logger.info("Test EARFCN Values Function Triggered")
    test = E_UTRA
    freq = dpg.get_value("Single_Band_Input")
    test.lookup_table(freq)
    logger.info(test.lookup_table(freq))
    bandwidth = 10

    match test.lookup_table(freq):
        case "71":
            logger.info(" Special Case for Band 71")
            special_case_1 = test.TABLE[test.lookup_table(freq)]
            fdl_low2 = special_case_1[0]
            noffs_dl2 = special_case_1[1]
            math3 = (float(freq) - fdl_low2) / 0.1 + noffs_dl2
            logger.info(math3)
            logger.info(math3 + 65536, math3, test.lookup_table(freq))
            with dpg.window(pos=(0, 680), height=55, width=550, no_close=True, no_collapse=True, no_scrollbar=True, no_move=True, no_title_bar=True):
                dpg.add_text(
                    f"{math3 + 65536, math3, int(test.lookup_table(freq)), bandwidth}")
                x = [
                    f"{math3 + 64536, math3, int(test.lookup_table(freq)), bandwidth}"]
                y = " ".join(x)
                logger.info(y)
                logger.debug(type(y))
                z = test.change_to_string(y)
                logger.info(z[0])
                logger.info(z[1])
                logger.info(z[2])
                logger.info(z[3])
                first = z[0]
                af_ulearfcn = first[1:-3]
                logger.debug(type(first))
                logger.info(af_ulearfcn)
                second = z[1]
                af_dlearfcn = second[:-3]
                logger.info(af_dlearfcn)
                third = z[2]
                af_bandnumber = third[:-1]
                logger.info(af_bandnumber)
                fourth = z[3]
                af_bandwidth = fourth[:-1]
                logger.info(af_bandwidth)
                dpg.set_value(item="ULEARFCN_VALUE", value=af_ulearfcn)
                dpg.set_value(item="DLEARFCN_VALUE", value=af_dlearfcn)
                dpg.set_value(item="BAND_VALUE", value=af_bandnumber)
                dpg.set_value(item="BW_VALUE", value=af_bandwidth)
        case "66":
            logger.info(" Special Case for Band 66")
            freq = dpg.get_value("Single_Band_Input")
            special_case_2 = test.TABLE[test.lookup_table(freq)]
            fdl_low3 = special_case_2[0]
            noffs_dl3 = special_case_2[1]
            math4 = (float(freq) - fdl_low3) / 0.1 + noffs_dl3
            logger.info(math4)
            logger.info(math4 + 64536, math4, test.lookup_table(freq))
            with dpg.window(pos=(0, 680), height=55, width=550, no_close=True, no_collapse=True, no_scrollbar=True, no_move=True, no_title_bar=True):
                dpg.add_text(
                    f"{math4 + 64536, math4, int(test.lookup_table(freq)), bandwidth}")
                x = [
                    f"{math4 + 64536, math4, int(test.lookup_table(freq)), bandwidth}"]
               # print(x[1])
                y = " ".join(x)
                logger.info(y)
                logger.debug(type(y))
                z = test.change_to_string(y)
                logger.info(z[0])
                logger.info(z[1])
                logger.info(z[2])
                logger.info(z[3])
                first = z[0]
                af_ulearfcn = first[1:-3]
                logger.debug(type(first))
                (af_ulearfcn)
                second = z[1]
                af_dlearfcn = second[:-3]
                logger.info(af_dlearfcn)
                third = z[2]
                af_bandnumber = third[:-1]
                logger.info(af_bandnumber)
                fourth = z[3]
                af_bandwidth = fourth[:-1]
                logger.info(af_bandwidth)
                dpg.set_value(item="ULEARFCN_VALUE", value=af_ulearfcn)
                dpg.set_value(item="DLEARFCN_VALUE", value=af_dlearfcn)
                dpg.set_value(item="BAND_VALUE", value=af_bandnumber)
                dpg.set_value(item="BW_VALUE", value=af_bandwidth)
        case _:
            try:
                logger.info(
                    " It's the default case, this is for every other band execpt for the special cases.")
                x = test.TABLE[test.lookup_table(freq)]
                fdl_low = x[0]
                noffs_dl = x[1]
                math = (float(freq) - fdl_low) / 0.1 + noffs_dl
                ulearfcn = math + 18000
                with dpg.window(pos=(0, 680), height=55, width=550, no_close=True, no_collapse=True, no_scrollbar=True, no_title_bar=True):
                    dpg.add_text(
                        f"{ulearfcn, math, int(test.lookup_table(freq)), bandwidth}")
                    x = [
                        f"{math + 18000, math, int(test.lookup_table(freq)), bandwidth}"]
                    y = " ".join(x)
                    logger.info(y)
                    logger.debug(type(y))
                    z = test.change_to_string(y)
                    logger.info(z[0])
                    logger.info(z[1])
                    logger.info(z[2])
                    logger.info(z[3])
                    first = z[0]
                    af_ulearfcn = first[1:-3]
                    logger.debug(type(first))
                    logger.info(af_ulearfcn)
                    second = z[1]
                    af_dlearfcn = second[:-3]
                    logger.info(af_dlearfcn)
                    third = z[2]
                    af_bandnumber = third[:-1]
                    logger.info(af_bandnumber)
                    fourth = z[3]
                    af_bandwidth = fourth[:-1]
                    logger.info(af_bandwidth)
                    dpg.set_value(item="ULEARFCN_VALUE", value=af_ulearfcn)
                    dpg.set_value(item="DLEARFCN_VALUE", value=af_dlearfcn)
                    dpg.set_value(item="BAND_VALUE", value=af_bandnumber)
                    dpg.set_value(item="BW_VALUE", value=af_bandwidth)
            except KeyError:
                logger.error("Popup Window triggered.")
                dpg.configure_item(item="popup_window", show=True)
