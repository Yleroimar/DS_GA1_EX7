import os

from utils.parser import init_parser
from utils.printing import *
from utils.ring import Ring


KEYWORD_KEY_SPACE = "#key-space"
KEYWORD_NODES = "#nodes"
KEYWORD_SHORTCUTS = "#shortcuts"


def read_ring_description(path: str) -> [str]:
    with open(path, "r", encoding="UTF-8") as f:
        return [line.strip() for line in f.read().strip().split("\n")]


def parse_ring_description(lines: [str]) -> ((int, int), [int], [(int, int)]):
    """
    :param lines: lines from the ring description file.
    :return: a triple of key-space start/end pair, node values and shortcuts
    """

    def find_description_line(description_comment: str) -> str:
        if description_comment not in lines:
            print_error_and_stop(f"Input file is missing comment '{description_comment}'!")

        i = lines.index(description_comment) + 1

        if len(lines) <= i:
            print_error_and_stop(f"Missing description after comment '{description_comment}'!")

        return lines[i]

    def parse_key_space() -> (int, int):
        key_start, key_end = find_description_line(KEYWORD_KEY_SPACE).split(",")
        return int(key_start.strip()), int(key_end.strip())

    def parse_node_values() -> [int]:
        values_str: [str] = find_description_line(KEYWORD_NODES).split(",")

        if len(values_str) == 0:
            print_error_and_stop("At least one node value is required!")

        return list(map(int, values_str))

    def parse_shortcuts() -> [(int, int)]:
        return [(int(start.strip()), int(end.strip()))
                for start, end in [pair.split(":")
                                   for pair in find_description_line(KEYWORD_SHORTCUTS).split(",")]]

    return parse_key_space(), parse_node_values(), parse_shortcuts()


def program_loop(ring: Ring):
    parse_entry = init_parser(ring)

    print_info("Starting program loop. Enter empty command to exit.")

    while True:
        entry = input("> ")

        if len(entry) == 0:
            return

        parse_entry(entry)


def usage():
    print("The program takes exactly 1 command-line argument: the input file detailing the ring.")


def get_file_path_from_args(args: [str]) -> str:
    if len(args) != 2:
        print_error("Wrong number of command line arguments were given!")
        usage()
        sys.exit(1)

    filename = args[1]

    if not os.path.exists(filename) or not os.path.isfile(filename):
        print_error_and_stop("Provided file does not exist or does not refer to a file!")

    return filename


def main(args: [str]):
    print_info("Reading description from input file...")
    description: [str] = read_ring_description(get_file_path_from_args(args))

    print_info("Parsing description...")
    (ks_start, ks_end), node_values, shortcuts = parse_ring_description(description)

    print_info("Initializing the ring...")
    program_loop(Ring(ks_start, ks_end, node_values, shortcuts))


if __name__ == '__main__':
    main(sys.argv)
