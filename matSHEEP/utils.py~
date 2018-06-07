import uuid
import os

if "SHEEP_HOME" in os.environ.keys():
    BASE_DIR = os.environ["SHEEP_HOME"]
else:
    BASE_DIR = os.environ["HOME"] + "/SHEEP"

CIRCUIT_DIR_MID = BASE_DIR + "/benchmark_inputs/mid_level/circuits/"
INPUTS_DIR_MID = BASE_DIR + "/benchmark_inputs/mid_level/inputs/TMP/"
EXECUTABLE_DIR = BASE_DIR + "/build/bin"

TMP_INPUTS_DIR = BASE_DIR + "/benchmark_inputs/mid_level/inputs/TMP"
if not os.path.exists(TMP_INPUTS_DIR):
    os.system("mkdir " + TMP_INPUTS_DIR)


TMP_PARAMS_DIR = BASE_DIR + "/benchmark_inputs/params/TMP"
if not os.path.exists(TMP_PARAMS_DIR):
    os.system("mkdir " + TMP_PARAMS_DIR)


def write_inputs_file(value_dict):
    """
    write k,v pairs into a file.  Randomly generate the filename
    and return to the user.
    """
    filename = TMP_INPUTS_DIR + "/inputs-" + str(uuid.uuid4()) + ".inputs"
    inputs_file = open(filename, "w")
    for k, v in value_dict.items():
        inputs_file.write(k + " " + str(v) + "\n")
    inputs_file.close()
    return filename


def write_params_file(param_dict):
    """
    write k,v pairs into a file.  Randomly generate the filename
    and return to the user.
    """
    filename = TMP_PARAMS_DIR + "/params-" + str(uuid.uuid4()) + ".params"
    params_file = open(filename, "w")
    for k, v in param_dict.items():
        params_file.write(k + " " + str(v) + "\n")
    params_file.close()
    return filename
