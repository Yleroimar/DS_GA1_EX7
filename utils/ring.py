from utils.distributed.node_ref import NodeRef
from utils.printing import print_warning, print_error
from utils.ring_ooc import RingOOC


class Ring:
    """
    Class representing the application's local back-end layer.
    Not to be confused with the distributed node-based back-end.

    With this layer we can perform for example lookups in step-by-step basis,
    where at each step a node returns the next node to lookup.

    This layer also prints errors and warnings, which occur in the distributed layer.
    In production software the printing would be of course only in front-end (CLI in our case).
    """


    def __init__(self, ks_bounds: (int, int), node_values: [int], shortcuts: [(int, int)]):
        self.__ks_start, self.__ks_end = ks_bounds
        self.__ooc: RingOOC = RingOOC(ks_bounds, node_values, shortcuts)


    def __is_in_key_space(self, key: int) -> bool:
        return self.__ks_start <= key <= self.__ks_end


    def __get_local_node(self) -> NodeRef:
        """ Method for getting the "local" node or in other words, the only node we know of. """
        # let's pretend like we are always aware of the smallest node
        return self.__ooc.get_lowest_node()


    def __get_local_node_value(self) -> int:
        return self.__get_local_node().get_value()


    def testing_list_as_str(self) -> str:
        """ OOC version of listing. Only used in testing. """
        return self.__ooc.list_as_str()


    def list_as_str(self) -> str:
        """
        Uses non-blocking approach:
          Free up node as soon as we are done with it.
          We simply ask a node for its description and then successor.
          Now we can leave it alone and make it available again, and move on to successor.

        :return: description of nodes in ring, starting from smallest node value
        """
        lines: [str] = []

        current: NodeRef = self.__ooc.get_lowest_node()
        visited: {NodeRef} = set()

        while current not in visited:
            visited.add(current)

            lines.append(str(current))
            current: NodeRef = current.get_successor()

        return "\n".join(lines)


    def lookup(self, target_key: int, starting_value: int or None = None) -> (NodeRef or None, int):
        if not self.__is_in_key_space(target_key):
            print_error(f"Lookup key {target_key} is outside of key-space!")
            return None, 0

        if starting_value is None:
            starting_value = self.__ooc.get_lowest_node_value()

        if starting_value not in self.__ooc:
            print_error(f"Lookup starting node with value {target_key} is not connected!")
            return None, 0

        return self.__perform_lookup(target_key, self.__ooc.get_node(starting_value))


    def __perform_lookup(self, target_key: int, starting_node: NodeRef = None) -> (NodeRef, int):
        if starting_node is None:
            starting_node = self.__get_local_node()

        current_node: NodeRef = starting_node
        n_requests: int = 0

        while target_key not in current_node:
            current_node: NodeRef = current_node.ask_lookup_direction(target_key)
            n_requests += 1

        return current_node, n_requests


    def __get_previous_key(self, key: int) -> int:
        assert self.__ks_start <= key <= self.__ks_end

        key -= 1

        return self.__ks_end if key < self.__ks_start else key


    def __find_preceding_node(self, node: NodeRef, searching_node: NodeRef = None) -> NodeRef:
        return self.__perform_lookup(self.__get_previous_key(node.get_keys_start()),
                                     node if searching_node is None else searching_node)[0]


    def join(self, value: int):
        if not self.__is_in_key_space(value):
            print_warning(f"Node with value {value} cannot join,"
                          " because it is outside of the key-space.")
            return

        successor, _ = self.__perform_lookup(value)

        if successor.get_value() == value:
            print_error(f"Node with value {value} cannot join,"
                        " because a node with same value is already connected.")
            return

        node: NodeRef = NodeRef(value)
        self.__ooc.ooc_memorize(node)

        successor_successor: NodeRef = successor.get_successor()

        # check if it is a single-node-ring
        if successor_successor == successor:
            node.set_successors(successor, node)
            successor.set_successors(node, successor)
            return

        # otherwise we also find the predecessors and notify them
        predecessor: NodeRef = self.__find_preceding_node(successor)
        predecessor_next: NodeRef = self.__find_preceding_node(predecessor, successor)

        node.set_successors(successor, successor_successor)
        predecessor.set_successors(node, successor)
        predecessor_next.set_successors(predecessor, node)


    def leave(self, value: int):
        if value not in self.__ooc:
            print_warning(f"Node with value {value} cannot leave,"
                          " because it has not even joined the ring.")
            return

        if len(self.__ooc) == 1:
            print_error(f"Node with value {value} cannot leave,"
                        " because less than one would remain.")
            return

        self.__ooc.terminate_node(value)

        self.refresh()


    def refresh(self):
        """ Here we perform a ring-wide refresh. """
        starting_node: NodeRef = self.__get_local_node()
        current_node: NodeRef = starting_node

        while True:
            current_node.refresh()
            current_node = current_node.get_successor()

            if current_node == starting_node:
                return


    def add_shortcut(self, start: int, end: int):
        for word, value in [("start", start), ("end", end)]:
            if not self.__is_in_key_space(value):
                print_error(f"Shortcut {word} node with value {value} is outside of the key-space.")
                return

        start_node: NodeRef = self.__perform_lookup(start)[0]
        if start_node.get_value() != start:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        "because start node is not in the network.")
            return

        end_node: NodeRef = self.__perform_lookup(end)[0]
        if end_node.get_value() != end:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        "because end node is not in the network.")
            return

        start_node.add_shortcut(end_node)
