'''
All the code in this file has been copied from
the original SHEEP package. This is necessary to make the
matSHEEP package easy to use.
'''

import uuid
import os
import re


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


def cleanup_time_string(t):
    """
    convert from microseconds to seconds, and only output 3 s.f.
    """
    time_in_seconds = float(t) / 1e6

    if time_in_seconds < 1:
        time_in_seconds = round(time_in_seconds, 5)
    else:
        time_in_seconds = int(time_in_seconds)
    timestring = str(time_in_seconds)
    return timestring


def parse_test_output(outputstring, debug_filename=None):
    """
    Extract values from the stdout output of the "benchmark" executable.
    return a dict in the format { "processing times (seconds)" : {},
    "outputs" : {}, "sizes" : {}, "params":{}, "sizes"{} }
    """
    results = {}
    processing_times = {}
    test_outputs = {}
    params = {}
    sizes = {}
    clear_check = {}
    in_results_section = False
    in_processing_times = False
    in_outputs = False
    if debug_filename:
        debugfile = open(debug_filename, "w")
# parse the file, assuming we have processing times then outputs.
    for line in outputstring.decode("utf-8").splitlines():
        if debug_filename:
            debugfile.write(line + "\n")
# read lines where parameters are printed out
        param_search = re.search("Parameter ([\S]+) = ([\d]+)", line)
        if param_search:
            params[param_search.groups()[0]] = param_search.groups()[1]
# read lines where sizes of keys or ciphertexts are printed out
        size_search = re.search("size of ([\S]+):[\s]+([\d]+)", line)
        if size_search:
            sizes[size_search.groups()[0]] = size_search.groups()[1]
        if in_results_section:
            # parse the check against clear context:
            if line.startswith("Cleartext check"):
                clear_check["is_correct"] = "passed OK" in line

            if in_processing_times:
                num_search = re.search("([\w]+)\:[\s]+([\d][\d\.e\+]+)", line)
                if num_search:
                    label = num_search.groups()[0]
                    processing_time = num_search.groups()[1]
                    processing_time = cleanup_time_string(
                        processing_time)  # and convert to seconds
                    processing_times[label] = processing_time
                if "Output values" in line:
                    in_processing_times = False
                    in_outputs = True
            elif in_outputs:
                output_search = re.search("([\w]+)\:[\s]+([-\d]+)", line)
                if output_search:
                    label = output_search.groups()[0]
                    val = output_search.groups()[1]
                    test_outputs[label] = val
                if "END RESULTS" in line:
                    in_results_section = False
            elif "Processing times" in line:
                in_outputs = False
                in_processing_times = True
        elif "=== RESULTS" in line:
            in_results_section = True
            pass
    results["Processing times (s)"] = processing_times
    results["Outputs"] = test_outputs
    results["Object sizes (bytes)"] = sizes
    results["Parameter values"] = params
    results["Cleartext check"] = clear_check
    if debug_filename:
        debugfile.close()
    return results
