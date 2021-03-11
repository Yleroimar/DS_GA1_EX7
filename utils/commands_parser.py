from typing import Callable

from utils.printing import print_warning, print_error, print_info
from utils.ring import Ring


""" Contains code for parsing commands of the program loop. """

CommandsParser = Callable[[str], None]
CommandImplementation = Callable[[str], None]


def initialize_commands(ring: Ring) -> {str: CommandImplementation}:
    command_to_implementation: {str: CommandImplementation} = dict()


    def lister(_: str):
        print(ring.list_as_str())


    command_to_implementation["List"] = lister


    def lookup(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Lookup <key value>(:<starting node value>)")
            return

        pieces = args_part.split(":")

        if not len(pieces) < 3:
            print_error(f"Lookup command received a wrong number of arguments: {pieces}.")
            return

        if not all(piece.isdecimal() for piece in pieces):
            print_error("Argument values need to be integers!")
            return

        node, n_requests = ring.lookup(int(pieces[0]),
                                       None if len(pieces) == 1 else int(pieces[1]))

        print(f"Result: Data stored in node {node.get_value()} - {n_requests} requests sent.")


    command_to_implementation["Lookup"] = lookup


    def join(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Join <joining node value>")
            return

        if not args_part.isdecimal():
            print_error(f"Join command received non-integer argument: '{args_part}'.")
            return

        ring.join(int(args_part))


    command_to_implementation["Join"] = join


    def leave(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Leave <leaving node value>")
            return

        if not args_part.isdecimal():
            print_error(f"Leave command received non-integer argument: '{args_part}'.")
            return

        ring.leave(int(args_part))


    command_to_implementation["Leave"] = leave


    def shortcut(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Shortcut <start node value>:<end node value>")
            return

        pieces = args_part.split(":")

        if len(pieces) != 2:
            print_error(f"Shortcut command received a wrong number of arguments: {pieces}.")
            return

        if not all(piece.isdecimal() for piece in pieces):
            print_error("Argument values need to be integers!")
            return

        ring.add_shortcut_indirect(int(pieces[0]), int(pieces[1]))


    command_to_implementation["Shortcut"] = shortcut


    def remove(args_part: str):
        print_error("Command 'Remove' is not implemented")
        # ring.leave([int(value_str.strip()) for value_str in args_part.split(",")])


    # command_to_implementation["Remove"] = remove

    return command_to_implementation


def init_command_parser(ring: Ring) -> CommandsParser:
    command_to_implementation: {str: CommandImplementation} = initialize_commands(ring)

    print_info("Available commands are:", ", ".join(command_to_implementation.keys()))


    def parse_entry(entry_full: str):
        pieces: [str] = entry_full.split(" ", maxsplit=1)

        command: str = pieces[0].strip()

        if command not in command_to_implementation:
            print_warning(f"No such command: '{command}'.")
        else:
            command_to_implementation[command]("" if len(pieces) == 1 else pieces[1].strip())


    return parse_entry
