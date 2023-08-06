import subprocess
import pathlib


def get_ip_script_output():
    """Fucntion that captures the output of checkipcon in python"""

    ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
    #print(ROOT)
    file2 = ROOT / "shell_scripts" / "checkipcon.sh"
    #print(file2)
    output = subprocess.check_output(["bash", f"{file2}"])
    output_to_string = str(output)
    #print(output_to_string)
    corrected_output = output_to_string[2:-3]
    #print(corrected_output)
    return corrected_output

