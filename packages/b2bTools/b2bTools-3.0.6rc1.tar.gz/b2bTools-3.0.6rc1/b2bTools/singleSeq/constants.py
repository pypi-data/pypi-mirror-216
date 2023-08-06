TOOL_DYNAMINE = 'dynamine'
TOOL_DISOMINE = 'disomine'
TOOL_EFOLDMINE = 'efoldmine'
TOOL_AGMATA = 'agmata'
TOOL_PSP = 'psper'

DEPENDENCIES = {
    TOOL_DYNAMINE: [],
    TOOL_DISOMINE: [TOOL_DYNAMINE, TOOL_EFOLDMINE],
    TOOL_EFOLDMINE: [TOOL_DYNAMINE],
    TOOL_AGMATA: [TOOL_DYNAMINE, TOOL_EFOLDMINE],
    TOOL_PSP: []
}

PREDICTOR_NAMES = [TOOL_DYNAMINE, TOOL_DISOMINE, TOOL_EFOLDMINE, TOOL_AGMATA, TOOL_PSP]
PREDICTION_NAMES = ["backbone", "sidechain", "ppII", "coil", "sheet", "helix", "earlyFolding", "agmata", "disoMine", "complexity", "arg", "tyr", "RRM", "disorder"]