import os

from utils.commands_parser import init_command_parser, CommandsParser
from utils.input_file_parser import *
from utils.printing import *
from utils.ring import Ring


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
