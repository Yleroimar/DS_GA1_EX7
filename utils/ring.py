from utils.node import Node
from utils.printing import print_error, print_warning, print_error_and_stop


class Ring:
    def __init__(self, ks_start: int, ks_end: int, node_values: [int], shortcuts: [(int, int)]):
        self.__ks_start: int = ks_start
        self.__ks_end: int = ks_end

        self.__nodes: {int: Node} = self.__create_nodes_and_assign_successors(node_values)

        self.add_shortcuts(shortcuts)

    def get_key_space_start(self) -> int:
        return self.__ks_start

    def get_key_space_end(self) -> int:
        return self.__ks_end

    def get_node(self, value: int) -> Node:
        return self.__nodes[value]

    def get_node_count(self) -> int:
        return len(self.__nodes)

    def __create_nodes_and_assign_successors(self, node_values: [int]) -> [Node]:
        if len(node_values) == 0:
            print_error_and_stop("No node values provided!"
                                 " Ring requires at least one node value for initialization!")

        nodes: [Node] = []

        for value in sorted(node_values):
            if self.__ks_start <= value <= self.__ks_end:
                nodes.append(Node(value, self.__ks_start, self.__ks_end))
            else:
                print_warning(f"Node value {value} is out of key-space! Discarding...")

        for node, successor, successor2 in zip(nodes, nodes[1:] + nodes[:1], nodes[2:] + nodes[:2]):
            node.set_successors(successor, successor2)

        return dict((node.value, node) for node in nodes)

    def add_shortcuts(self, shortcuts: (int, int)):
        for start, end in shortcuts:
            self.add_shortcut(start, end)

    def add_shortcut(self, start: int, end: int):
        self.__nodes[start].add_shortcut_to(self.__nodes[end])

    def list_as_str(self) -> str:
        return "\n".join(str(node)
                         for _, node in sorted(self.__nodes.items(), key=lambda pair: pair[0]))

    def lookup(self, target_key: int, starting_value: int or None = None) -> (int, int) or None:
        if not self.__ks_start <= target_key <= self.__ks_end:
            print_error(f"Lookup key {target_key} is outside of key-space!")
            return None

        if starting_value is None:
            starting_value = min(self.__nodes.keys())

        return self.__nodes[starting_value].lookup(target_key)

    def find_proceeding_node(self, node: Node) -> Node:
        """
        **NB! Functionality breaks if there is a node with invalid successor references.**

        :param node: node for which we are finding the (would-be) proceeding node.
        :return: the node that proceeds or would proceed the given node.
        """
        current_node: Node = min(self.__nodes.values())

        while current_node <= node:
            successor: Node = current_node.successor

            if successor <= current_node:
                return successor

            current_node = successor

        return current_node

    def join(self, node_value: int):
        if not self.__ks_start <= node_value <= self.__ks_end:
            print_warning(f"Node with value {node_value} cannot join,"
                          f" because it is outside of the key-space.")
            return

        if node_value in self.__nodes:
            print_warning(f"Node with value {node_value} cannot join,"
                          " because it has already joined.")
            return

        new_node: Node = Node(node_value, self.__ks_start, self.__ks_end)

        new_node.refresh_successors_join(self.find_proceeding_node(new_node))

        self.__nodes[node_value] = new_node

    def leave(self, node_values: [int]):
        """ Covers both the case where a single node leaves and where multiple nodes leave. """

        nodes_leaving: {Node} = set()

        for value in node_values:
            if not self.__ks_start <= value <= self.__ks_end:
                print_warning(f"Node value {value} is outside of the key-space."
                              " Discarding value...")
                continue

            if value not in self.__nodes:
                print_warning(f"Node with value {value} has already left.")
                continue

            nodes_leaving.add(value)

        n_leaving: int = len(nodes_leaving)

        if n_leaving == 0:
            print_warning("All leaving nodes have already left or are not in the key-space.")
            return

        if n_leaving < len(node_values):
            print_warning("Some nodes have requested to leave more than once...")

        if len(self.__nodes) <= n_leaving:
            print_error("Nodes cannot leave, less than one would remain.")
            return

        chain_start: Node = self.__nodes[list(nodes_leaving)[0]]

        for node_value in nodes_leaving:
            self.__nodes.pop(node_value).prepare_to_leave()

        (chain_start := chain_start.get_non_leaving_successor()) \
            .refresh_refs_leave(chain_start.get_non_leaving_successor())

    def remove_shortcuts_to(self, node: Node):
        for from_node in self.__nodes.values():
            finger_table = from_node.finger_table

            if node in finger_table:
                finger_table.remove(node)
