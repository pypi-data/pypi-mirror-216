# s60z
## Purpose
- Change channels on the Software Defined Radio (SDR) with a Graphical User Interface (GUI) that allows for either set parameters to be autofilled or with custom inputs.
## Requirments
- In order for this GUI to be functional, the host computer the GUI is run on must be connected via ethernet to a powered S60Z AP Module, Model 470Z SDR. The wired IP address of the host computer must match the subnet of the SDR which has a static IP address, which is 10.10.40.201. For example, the Host Computer's wired IP address can be as follows 10.10.40.202, mathcing the subnet of the static Ip address found on the SDR to ensure proper connection and intergration. This device was manufactured by ip.Access, and more information for the device can be found in their documentation. 
## Synopsis 
- Gui button prompts, or 4 inputs that you can manually type in to display a differnt frequency within the capabilities of the SDR. 
## Description 
- The current scripts that come with the SDR are not simplified enough for effecient use in demos. The purpose of creating a new Gui is to simplify the process of changing frequencies (channels) with a series of scripts and commands that handle the bulk of the work. The GUI will display information regarding the Band Number and Bandwidth as well as the information regarding the MHZ of the Bandwidth. After pressing the button, it will auto fill the parameters as needed and send that information to the SDR. The bottom portion of the GUI allows for user input. where you are able to input custom values for the EARFCN UL, DL, Band Number, and Bandwidth in case the user wants more control over the specific frequency. The values for EARFCN UL and DL must be close to the middle values specified on Squimway in order to work. If there is an error with any of these inputs, a popup window will display detailing the issue that has been found.
- The purpose of this program is to create a graphical user interface (GUI) using dearpygui, a python module, to simplify the Band Changing Process for the S60z software-defined radio (SDR). For this program to work, you need a specific hardware configuration. 
- To power the S60z, a 12V DC power source is required. The S60z should be accompanied by a sufficient power supply for use.
-  This program works by integrating scripts present on both the SDR and the host computer. To work, all scripts required must be present on both devices. 
-  The S60z works on a yocto-based Linux operating system, and the host computer is expected to be operating on Arch Linux. 
-  A hard-wired ethernet connection between the host computer and the SDR is required for operational use. The wired subnet of the host computer must match that of the I.P. address of the SDR. The I.P. address of the SDR is a static IP address and can be found on a note located physically on the SDR. If the subnets do not match, it is not possible to execute commands via SSH (a secure shell network protocol), because these two pieces of hardware will communicate solely over a network.
-   Once the S60z hardware has been configured properly, and connected to the host computer with a correct wired I.P. address subnet, and the proper scripts can be located and found on both devices, you can run this script.
-    Upon launch, the script will open a GUI on the host computer that will display interactive buttons with RF (radio frequency) information on them. The user will be able to then change the Band of the signal they are currently generating at the click of a button by remotely executing a range of commands from the host computer based on set parameters found in the script below. 
-    A Custom Input field for values is also currently in development.


![animatedGIF](https://github.com/cellantenna/s60z/assets/127258036/276411a4-7e82-4590-a51a-7edc4f22a49c)
