from typing import Callable, Optional

from utils.printing import print_warning, print_error, print_info
from utils.local_backend import LocalBackend


""" Contains code for parsing commands of the program loop. """

CommandsParser = Callable[[str], None]
CommandImplementation = Callable[[str], None]


def initialize_commands(ring: LocalBackend) -> {str: CommandImplementation}:
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

        target_key: int = int(pieces[0])
        starting_node: Optional[int] = None if len(pieces) == 1 else int(pieces[1])

        node, n_requests = ring.lookup(target_key, starting_node)

        if node is None:
            print_info(f"Could not find the key {target_key}.")
        else:
            print(f"Result: Data stored in node {node.get_value()} - {n_requests} requests sent.")


    command_to_implementation["Lookup"] = lookup


    def join(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Join <joining node value>")
            return

        if not args_part.isdecimal():
            print_error(f"Join command received non-integer argument: '{args_part}'.")
            return

        joiner_value: int = int(args_part)

        print_info(f"Node with value {joiner_value} is trying to join the ring.")
        print_info(f"Node with value {joiner_value} has "
                   + ("successfully joined" if ring.join(joiner_value) else "not joined")
                   + " the ring.")


    command_to_implementation["Join"] = join


    def leave(args_part: str):
        if len(args_part) == 0:
            print_info("Usage: Leave <leaving node value>")
            return

        if not args_part.isdecimal():
            print_error(f"Leave command received non-integer argument: '{args_part}'.")
            return

        leaver_value: int = int(args_part)

        print_info(f"Node with value {leaver_value} is trying to leave the ring.")
        print_info(f"Node with value {leaver_value} "
                   + ("has successfully"
                      if ring.leave(leaver_value)
                      else "could not or had already")
                   + " left the ring.")


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

        start, end = int(pieces[0]), int(pieces[1])

        print_info(f"Trying to add a shortcut from node {start} to node {end}.")
        print_info(f"Shortcut from node {start} to node {end} "
                   + ("was" if ring.add_shortcut(start, end) else "could not be")
                   + " added to the ring.")


    command_to_implementation["Shortcut"] = shortcut

    # def remove(args_part: str):
    #     print_error("Command 'Remove' is not implemented")

    # command_to_implementation["Remove"] = remove

    return command_to_implementation


def print_available_commands(command_to_implementation: {str: CommandImplementation}):
    print_info("Available commands are:", ", ".join(command_to_implementation.keys()))


def init_command_parser(ring: LocalBackend) -> CommandsParser:
    command_to_implementation: {str: CommandImplementation} = initialize_commands(ring)

    print_available_commands(command_to_implementation)


    def parse_entry(entry_full: str):
        pieces: [str] = entry_full.split(" ", maxsplit=1)

        command: str = pieces[0].strip()

        if command not in command_to_implementation:
            print_warning(f"No such command: '{command}'.")
            print_available_commands(command_to_implementation)
            return

        command_to_implementation[command]("" if len(pieces) == 1 else pieces[1].strip())


    return parse_entry
