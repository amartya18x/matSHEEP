from reusable_modules import oneb_adder
from particles import variables
from utils import parse_test_output
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
        results["circuit_name"] = self.name
        results["num_inputs"] = self.num_inputs
        return results


if __name__ == '__main__':
    x = variables('x')
    y = variables('y')
    cin = variables('cin')
    s = variables('sum')
    c = variables('carry')
    b2_adder = oneb_adder('2b_adder', [x, y, cin], [s, c], 1)
    circuit = circuit('2 Bit Adder', b2_adder)
    circuit.write_file(filename='./test.sheep')
