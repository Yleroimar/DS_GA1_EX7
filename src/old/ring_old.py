from src.old.node_old import Node
from src.printing import *


# import random


# random.seed(1337)


class Ring:
    """
    A place to store nodes in.
    Also keeps track of and checks key-space boundaries.
    The key-space boundaries could otherwise be kept in data objects,
     which nodes would hold a reference to.
    """


    def __init__(self, ks_start: int, ks_end: int, node_values: [int], shortcuts: [(int, int)]):
        self.__ks_start: int = ks_start
        self.__ks_end: int = ks_end

        self.__nodes: {int: Node} = self.__create_nodes_and_assign_successors(node_values)

        self.__add_shortcuts(shortcuts)


    def __create_nodes_and_assign_successors(self, node_values: [int]) -> {int: Node}:
        valid_values: {int} = set()

        for value in node_values:
            if self.is_in_key_space(value):
                valid_values.add(value)
            else:
                print_warning(f"Node value {value} is out of key-space! Discarding...")

        if len(valid_values) == 0:
            print_error_and_stop("No (suitable) node values provided!"
                                 " Ring requires at least one node value for initialization!")

        nodes: [Node] = [Node(value) for value in sorted(valid_values)]

        for node, successor, successor2 in zip(nodes, nodes[1:] + nodes[:1], nodes[2:] + nodes[:2]):
            node.set_successors(successor, successor2)

        return dict((node.get_value(), node) for node in nodes)


    def __add_shortcuts(self, shortcuts: [(int, int)]):
        for start, end in shortcuts:
            self.add_shortcut_indirect(start, end)


    def is_in_key_space(self, key: int) -> bool:
        return self.__ks_start <= key <= self.__ks_end


    def __pick_random_node(self) -> Node:
        """ To better simulate decentralization. """
        return min(self.__nodes.values())  # for the sake of determinism, I'll pick the min for now
        # return random.choice(list(self.__nodes.values()))


    def list_as_str(self) -> str:
        return min(self.__nodes.values()).list_as_str()


    def testing_list_as_str(self) -> str:
        """ A version of listing, which breaks the decentralization rule. Only used in testing. """
        return "\n".join(str(node) for node in sorted(self.__nodes.values()))


    def get_node(self, node_value: int) -> Node:
        """ Solely used by unit tests for key ranges. """
        return self.__nodes[node_value]


    def lookup(self, target_key: int, starting_value: int or None = None) -> (int or None, int):
        if not self.is_in_key_space(target_key):
            print_error(f"Lookup key {target_key} is outside of key-space!")
            return None, 0

        if starting_value is None:
            starting_value = min(self.__nodes.keys())

        return self.__nodes[starting_value].lookup(target_key)


    def join(self, node_value: int):
        if not self.is_in_key_space(node_value):
            print_warning(f"Node with value {node_value} cannot join,"
                          " because it is outside of the key-space.")
            return

        new_node: Node or None = self.__pick_random_node().handle_joiner(node_value)

        if new_node is not None:
            self.__nodes[node_value] = new_node


    def leave(self, node_value: int):
        if node_value not in self.__nodes:
            print_warning(f"Node with value {node_value} cannot leave,"
                          " because it has not even joined the ring.")
            return

        if len(self.__nodes) == 1:
            print_error(f"Node with value {node_value} cannot leave,"
                        " because less than one would remain.")
            return

        self.__nodes[node_value].leave()
        self.__nodes.pop(node_value)
        self.__pick_random_node().refresh()


    def add_shortcut_indirect(self, start: int, end: int):
        if start not in self.__nodes:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        "because start node is not in the network.")
            return

        self.__nodes[start].add_shortcut_by_value(end)


    def add_shortcut_direct(self, start: int, end: int):
        """
        Adding shortcuts directly if both nodes are known.
        Task instructions were not clear enough on restrictions,
         so I also implemented Ring.add_shortcut()
        """
        if start not in self.__nodes or end not in self.__nodes:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        "because start and/or end node is not in the network.")
            return

        self.__nodes[start].add_shortcut(self.__nodes[end])
