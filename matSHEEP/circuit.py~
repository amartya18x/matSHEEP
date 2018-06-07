from reusable_modules import oneb_adder
from particles import variables
from frontend.utils import parse_test_output, get_bitwidth
from frontend.database import BenchmarkMeasurement, session
import os
import subprocess

if "SHEEP_HOME" in os.environ.keys():
    BASE_DIR = os.environ["SHEEP_HOME"]
else:
    BASE_DIR = os.environ["HOME"] + "/SHEEP"

CIRCUIT_DIR_MID = BASE_DIR + "/benchmark_inputs/mid_level/circuits/"
INPUTS_DIR_MID = BASE_DIR + "/benchmark_inputs/mid_level/inputs/TMP/"
EXECUTABLE_DIR = BASE_DIR + "/build/bin"


class circuit(object):
    def __init__(self, name, circuit,
                 const_inputs=[]):
        self.name = name

        self.circuit = circuit
        self.const_inputs = const_inputs
        self.flag_inputs = ['TRUE', 'FALSE']
        self.on_file = False

    def get_inputs(self):
        assert self.circuit is not None
        self.const_inputs = self.const_inputs  # + self.circuit.const_inputs
        self.inputs = self.circuit.inputs
        self.outputs = self.circuit.outputs
        self.num_inputs = len(self.circuit.inputs)

    def output_circuit(self, filename):
        with open(filename, 'wb') as outfile:
            outfile.write("CONST_INPUTS")
            outfile.write("\n")
            outfile.write("INPUTS ")
            for ci in self.flag_inputs:
                outfile.write(" " + ci)
            for i in self.inputs.get_variables():
                outfile.write(" " + i)
            outfile.write("\n")
            outfile.write("OUTPUTS ")
            for o in self.outputs.get_variables():
                outfile.write(" " + o)
            outfile.write("\n")
            outfile.write(str(self.circuit))
            outfile.write("\n")

    def write_file(self, filename=None):
        self.get_inputs()
        self.on_file = True
        if filename is None:
            self.write_default_file()
        else:
            self.write_spec_file(filename)

    def write_default_file(self):
        filename = CIRCUIT_DIR_MID + self.name + ".sheep"
        self.filename = filename
        self.output_circuit(filename=filename)

    def write_spec_file(self, filename):
        self.filename = filename
        self.output_circuit(filename=filename)

    def run_circuit(self, inputs_file, input_type='bool', context='TFHE',
                    eval_strategy="parallel",
                    params_file=None, debugfilename=None):
        """
        run the circuit and retrieve the results.
        """
        run_cmd = []
        assert self.on_file, "Circuit needs to be written to file"
        run_cmd.append(os.path.join(EXECUTABLE_DIR, "benchmark"))
        run_cmd.append(self.filename)
        run_cmd.append(context)
        run_cmd.append(input_type)
        run_cmd.append(inputs_file)
        run_cmd.append(eval_strategy)
        if params_file:
            run_cmd.append(params_file)
        p = subprocess.Popen(args=run_cmd, stdout=subprocess.PIPE)
        job_output = p.communicate()[0]
        results = parse_test_output(job_output, debugfilename)
        # now just add other fields into the "results" dict, to go into the db
        results["context"] = context
        input_bitwidth = get_bitwidth(input_type)
        input_signed = input_type.startswith("i")
        results["input_bitwidth"] = input_bitwidth
        results["input_signed"] = input_signed
        circuit_name, num_inputs = self.name, self.num_inputs
        results["circuit_name"] = circuit_name
        results["num_inputs"] = num_inputs
        upload_measurement(results)
        return results


def upload_measurement(results):
    """
    insert a single benchmark run into the database.
    """
    execution_time = results["Processing times (s)"]["circuit_evaluation"]
    is_correct = results["Cleartext check"]["is_correct"]
    sizes = results["Object sizes (bytes)"]
    ciphertext_size = sizes["ciphertext"]
    public_key_size = sizes["publicKey"]
    private_key_size = sizes["privateKey"]
    param_dict = results["Parameter values"]

    m = BenchmarkMeasurement(context_name=results["context"],
                             input_bitwidth=results["input_bitwidth"],
                             input_signed=results["input_signed"],
                             execution_time=execution_time,
                             is_correct=is_correct,
                             ciphertext_size=ciphertext_size,
                             public_key_size=public_key_size,
                             private_key_size=private_key_size)
# the next two will be filled for low-level benchmarks
    if "gate_name" in results.keys():
        m.gate_name = results["gate_name"]
    if "depth" in results.keys():
        m.depth = results["depth"]
# these two will be filled for mid-level benchmarks
    if "circuit_name" in results.keys():
        m.circuit_name = results["circuit_name"]
    if "num_inputs" in results.keys():
        m.num_inputs = results["num_inputs"]
# the following two are unlikely to be filled for now..
    if "num_slots" in results.keys():
        m.num_slots = results["num_slots"]
    if "tbb_enabled" in results.keys():
        m.tbb_enabled = results["tbb_enabled"]
# now fill the parameter columns for the chosen context

    # only have HElib, not HElib_F2 and HElib_Fp
    context_prefix = results["context"].split("_")[0]
    for k, v in param_dict.items():
        column = context_prefix + "_" + k
        m.__setattr__(column, v)
# commit to the DB
    session.add(m)
    session.commit()


if __name__ == '__main__':
    x = variables('x')
    y = variables('y')
    cin = variables('cin')
    s = variables('sum')
    c = variables('carry')
    b2_adder = oneb_adder('2b_adder', [x, y, cin], [s, c], 1)
    circuit = circuit('2 Bit Adder', b2_adder)
    circuit.write_file(filename='./test.sheep')
