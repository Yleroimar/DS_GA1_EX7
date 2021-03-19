import os

from utils.commands_parser import init_command_parser, CommandsParser
from utils.printing import *
from utils.ring import Ring


def read_ring_description(path: str) -> [str]:
    with open(path, "r", encoding="UTF-8") as f:
        return f.read().split("\n")


def parse_ring_description(lines: [str]) -> ((int, int), [int], [(int, int)]):
    """
    :param lines: lines from the ring description file (assumed to be correctly formatted).
    :return: a triple of key-space start/end pair, node values and shortcuts
    """

    lines = [line
             for line in [line.strip() for line in lines]
             if 0 < len(line) and not line.startswith("#")]

    key_min, key_max = [int(piece.strip()) for piece in lines[0].split(",")]

    node_values = [int(piece.strip()) for piece in lines[1].split(",")]

    comma_split = [piece.split(":") for piece in lines[2].split(",")]
    shortcuts = ([]
                 if len(lines) < 3
                 else [(int(source.strip()), int(target.strip()))
                       for source, target in comma_split])

    return (key_min, key_max), node_values, shortcuts


def program_loop(ring: Ring):
    print_info("Initiating command parser.")
    parse_command: CommandsParser = init_command_parser(ring)

    print_info("Starting program loop. Enter empty command to exit.")

    while True:
        entry: str = input("> ")

        if len(entry) == 0:
            print_info("Empty input provided. Exiting...")
            return

        parse_command(entry)


def usage():
    print("The program takes exactly 1 command-line argument: the input file detailing the ring.")


def get_file_path_from_args(args: [str]) -> str:
    if len(args) != 2:
        print_error("Wrong number of command line arguments were given!")
        usage()
        sys.exit(1)

    filename: str = args[1]

    if not os.path.exists(filename) or not os.path.isfile(filename):
        print_error_and_stop("Provided file does not exist or does not refer to a file!")

    return filename


def main(args: [str]):
    input_file_path: str = get_file_path_from_args(args)

    print_info("Reading description from input file...")
    description: [str] = read_ring_description(input_file_path)

    print_info("Parsing description...")
    ks_bounds, node_values, shortcuts = parse_ring_description(description)

    print_info("Initializing the ring...")
    program_loop(Ring(ks_bounds, node_values, shortcuts))


if __name__ == '__main__':
    main(sys.argv)
