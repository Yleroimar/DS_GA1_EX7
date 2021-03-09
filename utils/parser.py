from utils.printing import print_warning, print_error
from utils.ring import Ring


def initialize_commands(ring: Ring) -> {str, callable}:
    command_to_implementation: {str: callable} = dict()

    def lister(_: str):
        print(ring.list_as_str())

    command_to_implementation["List"] = lister

    def lookup(args_part: str):
        pieces = args_part.split(":")

        if not 0 < len(pieces) < 3:
            print_error(f"Lookup command received a wrong number of arguments: {pieces}.")
            return

        node, n_requests = ring.lookup(int(pieces[0]),
                                       None if len(pieces) == 1 else int(pieces[1]))

        print(f"Result: Data stored in node {node} - {n_requests} requests sent.")

    command_to_implementation["Lookup"] = lookup

    def join(args_part: str):
        if not args_part.isnumeric():
            print_error(f"Join command received non-numeric argument: '{args_part}'.")
            return

        ring.join(int(args_part))

    command_to_implementation["Join"] = join

    def leave(args_part: str):
        ring.leave([int(args_part)])

    command_to_implementation["Leave"] = leave

    def remove(args_part: str):
        ring.leave([int(value_str.strip()) for value_str in args_part.split(",")])

    command_to_implementation["Remove"] = remove

    def shortcut(args_part: str):
        pieces = args_part.split(":")

        if len(pieces) != 2:
            print_error(f"Shortcut command received a wrong number of arguments: {pieces}.")
            return

        ring.add_shortcut(int(pieces[0]), int(pieces[1]))

    command_to_implementation["Shortcut"] = shortcut

    return command_to_implementation


def init_parser(ring: Ring) -> callable:
    command_to_implementation: {str, callable} = initialize_commands(ring)

    def parse_entry(entry_full: str):
        pieces = entry_full.split(" ", maxsplit=1)

        command = pieces[0].strip()

        if command not in command_to_implementation:
            print_warning(f"No such command: '{command}'.")
        else:
            command_to_implementation[command]("" if len(pieces) == 1 else pieces[1].strip())

    return parse_entry
