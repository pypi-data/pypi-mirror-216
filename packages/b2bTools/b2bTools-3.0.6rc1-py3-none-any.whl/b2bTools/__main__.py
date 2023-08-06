# Example for single sequence:
# python -m b2bTools -mode singleSeq \                                                                                                                                                          1 ↵
#     -dynamine \
#     -disomine \
#     -efoldmine \
#     -psper \
#     -agmata \
#     -file ../../../sandbox/testing/RdRp-Iposcan-800Reviewed.clean.tail.txt  \
#     -output ../../../sandbox/testing/RdRp-Iposcan-800Reviewed.clean.tail.json \
#     -index ../../../sandbox/testing/RdRp-Iposcan-800Reviewed.clean.tail.csv

import json
import sys
import os
from .wrapper_source.wrapper_utils import *

def print_help_section():
    print("Help section:")
    print("Show help section: --help or -h")
    print("An input file in FASTA format is required: -file /path/to/file.fasta")
    print("An output file path is required: -output /path/to/output_file.json")
    print("An output index file path is required: -index /path/to/output_file.csv")
    print("At least one predictor should be present:")
    print("AgMata: -agmata or -aggregation")
    print("Dynamine: -dynamine or -dynamics")
    print("Disomine: -disomine or -disorder")
    print("EFoldMine: -efoldmine or -early_folding_events")
    print("PSPer: -psp or -psper")
    print("An identifier is required: -identifier name")
    print("Full documentation available on https://pypi.org/project/b2bTools/")
    exit(0)

def single_sequence_flow(user_input_params):
    outputIndex_filepath = os.path.realpath(user_input_params.outputIndexFileName)

    single_seq = SingleSeq(user_input_params.fileName, user_input_params.short_id).predict(user_input_params.tools)

    print("All predictions have been executed. Next step: exporting the results")
    all_predictions = single_seq.get_all_predictions()
    with open(user_input_params.output_filepath, 'w') as json_file_handler:
        json.dump(all_predictions, json_file_handler, indent=2)

    if user_input_params.outputIndexFileName is not None:
        print("All predictions have been executed. Next step: exporting the index")
        single_seq.index(outputIndex_filepath, os.path.basename(user_input_params.output_filepath))

def msa_flow(user_input_params):
    msa = MultipleSeq()
    msa.from_aligned_file(path_to_msa=user_input_params.fileName, tools=user_input_params.tools)

    if len(user_input_params.plot_sequences) > 0:
        plots = msa.new_plot(selected_prot_labels=user_input_params.plot_sequences)
        for plot_index, plot in enumerate(plots):
            plot_filename = os.path.join(user_input_params.plot_dir, f'{plot_index}.png')
            plot.save(plot_filename)

    # if user_input_params.aggregated_plot:
        # msa.new_aggregated_plot()

class UserInputParams:
    def __init__(self):
        self.tools = []
        self.fileName = None
        self.outputFileName = None
        self.mode = None
        self.outputIndexFileName = None
        self.identifier = None
        self.short_id = False
        self.aggregated_plot = False
        self.plot_sequences = []
        self.plot_dir = None

    def is_single_seq_mode(self):
        return self.mode == 'singleSeq'

    def is_msa_mode(self):
        return self.mode == 'msa'

if __name__ == '__main__':
    _command, *parameters = sys.argv
    print("Bio2Byte Tools - Command Line Interface")

    user_input_params = UserInputParams()

    for index, param in enumerate(parameters):
        if param == "--help" or param == "-h":
          print_help_section()
        if param == "-short-id":
            user_input_params.short_id = True
        if param == "-file":
          user_input_params.fileName = parameters[index + 1]
        if param == "-output":
          user_input_params.outputFileName = parameters[index + 1]
        if param == "-mode":
          user_input_params.mode = parameters[index + 1]

          if not user_input_params.mode in ['singleSeq', 'msa']:
              exit("Invalid mode")

        if param == "-identifier":
          user_input_params.identifier = parameters[index + 1]
        if param == "-dynamics" or param == "-{0}".format(constants.TOOL_DYNAMINE):
            user_input_params.tools.append(constants.TOOL_DYNAMINE)
        if param == "-aggregation" or param == "-{0}".format(constants.TOOL_AGMATA):
            user_input_params.tools.append(constants.TOOL_AGMATA)
        if param == "-early_folding_events" or param == "-{0}".format(constants.TOOL_EFOLDMINE):
            user_input_params.tools.append(constants.TOOL_EFOLDMINE)
        if param == "-disorder" or param == "-{0}".format(constants.TOOL_DISOMINE):
            user_input_params.tools.append(constants.TOOL_DISOMINE)
        if param == "-psp" or param == "-{0}".format(constants.TOOL_PSP):
            user_input_params.tools.append(constants.TOOL_PSP)
        if param == "-index":
            user_input_params.outputIndexFileName = parameters[index + 1]
        if param == "-aggregated-plot":
            user_input_params.aggregated_plot = True
        if param == "-plot" and parameters[index + 1].startswith('"'):
            user_input_params.plot_sequences = parameters[index + 2].split(',')
        if param == "-plot" and not parameters[index + 1].startswith('"'):
            user_input_params.plot_sequences = ['all']
        if param == "-plot-dir":
            user_input_params.plot_dir = parameters[index + 1]

    if len(user_input_params.tools) == 0:
        exit("At least one predictor should be present: -agmata, -dynamine, -disomine, -efoldmine")
    if not user_input_params.fileName:
        exit("An input file is required: -file /path/to/file")
    if not user_input_params.outputFileName:
        exit("An output file path is required: -output /path/to/output_file.json")
    if not user_input_params.mode:
        exit("A mode is required: -mode (singleSeq or msa)")
    if (user_input_params.aggregated_plot or len(user_input_params.plot_sequences) > 0) and not user_input_params.plot_dir:
        exit("An output path for plots is required: -plot-dir /path")

    user_input_params.output_filepath = os.path.realpath(user_input_params.outputFileName)

    if user_input_params.is_single_seq_mode and not user_input_params.outputIndexFileName:
        exit("An output index file path is required: -index /path/to/output_file.csv")

    if user_input_params.is_single_seq_mode:
        print("Bio2Byte Tools - Single Sequence Analysis")
        single_sequence_flow(user_input_params)
    elif user_input_params.is_msa_mode:
        print("Bio2Byte Tools - Multiple Sequence Alignment Analysis")
        msa_flow(user_input_params)
    else:
        exit("Unexpected mode.")

    exit(0)
