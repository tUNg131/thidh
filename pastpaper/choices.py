BLANK_OPTIONS = "---"
DEFAULT_OPTIONS = ["A", "B", "C", "D"]


def get_choice_tuples(options):
    return [(str(i), o) for i, o in zip(range(len(options)), options)]


def get_choice_tuples_with_blank(options):
    return ["n", BLANK_OPTIONS] + get_choice_tuples(options)