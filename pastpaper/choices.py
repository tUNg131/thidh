MODEL_BLANK_CHAR = "n"
BLANK_TEXT = "---"
DEFAULT_OPTIONS = ["A", "B", "C", "D"]


def get_choice_tuples(options=DEFAULT_OPTIONS):
    return [(str(i), o) for i, o in zip(range(len(options)), options)]


def get_choice_tuples_with_blank(**kwargs):
    return [MODEL_BLANK_CHAR, BLANK_TEXT] + get_choice_tuples(**kwargs)