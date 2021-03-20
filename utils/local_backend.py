from typing import Optional

from utils.distributed.node_ref import NodeRef
from utils.printing import print_warning, print_error
from utils.ring_ooc import RingOOC


class LocalBackend:
    """
    Class representing the application's local back-end layer.
    Not to be confused with the distributed node-based back-end.

    With this layer we can perform for example lookups in step-by-step basis,
    where at each step a node returns the next node to lookup.

    This layer also prints errors and warnings, which occur in the distributed layer.
    """


    def __init__(self, ks_bounds: (int, int), ring: RingOOC):
        self.__ks_start, self.__ks_end = ks_bounds
        self.__ooc: RingOOC = ring


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


    def lookup(self, target_key: int,
               starting_value: Optional[int] = None) -> (Optional[NodeRef], int):
        """
        Uses non-blocking approach:
          Free up node as soon as we are done with it.
          We simply ask nodes where if they have the key
          or where to look for the targeted key value.
          Then we can leave it alone and make it available again, and move to the returned node.

        :param target_key: the key value to look for in the ring.
        :param starting_value: starting value which to start the lookup from.
            By default the lookup starts from the node with smallest value.
        :return: A pair of key-containing node reference (optional) and lookup request count.
            The lookup count is the number of times moved between nodes
            (the number of lookup directions received).
        """

        if not self.__is_in_key_space(target_key):
            print_error(f"Lookup key {target_key} is outside of key-space!")
            return None, 0

        if starting_value is None:
            starting_value: int = self.__ooc.get_lowest_node_value()

        if starting_value not in self.__ooc:
            print_error(f"The lookup starting node with value {starting_value} is not connected!")
            return None, 0

        return self.__perform_lookup(target_key, self.__ooc.get_node(starting_value))


    def __perform_lookup(self, target_key: int,
                         starting_node: Optional[NodeRef] = None) -> (NodeRef, int):
        if starting_node is None:
            starting_node = self.__get_local_node()

        current_node: NodeRef = starting_node
        n_requests: int = 0

        while target_key not in current_node:
            current_node: NodeRef = current_node.ask_lookup_direction(target_key)
            n_requests += 1

        return current_node, n_requests


    def __get_previous_key(self, key: int) -> int:
        assert self.__ks_start <= key <= self.__ks_end + 1

        key -= 1

        return self.__ks_end if key < self.__ks_start else key


    def __find_preceding_node(self, node: NodeRef,
                              searching_node: Optional[NodeRef] = None) -> NodeRef:
        return self.__perform_lookup(self.__get_previous_key(node.get_keys_start()),
                                     node if searching_node is None else searching_node)[0]


    def join(self, value: int) -> bool:
        """
        Here we utilize the previously declared action *lookup*.

            First we find the successor for the joining node by performing lookup using the joiner
        node value. If the returned node has the same value, we cannot proceed with joining,
        because values collide.

            We start the new joiner node. In the real world it would already be started,
        but here we try to minimize socket closing handling.

            We check if the ring is a single-node ring, in which case we can directly set the
        successors of the joiner and successor nodes. Otherwise we also find both predecessors by
        lookup on successor using the preceding key values of key range starts of the successor
        and the first predecessor.

            Finally, we update successors of both predecessors and the joiner node.

        :param value: the value of the joining node.
        :return: whether joining was successful or not.
        """

        if not self.__is_in_key_space(value):
            print_warning(f"Node with value {value} cannot join,"
                          " because it is outside of the key-space.")
            return False

        successor, _ = self.__perform_lookup(value)

        if successor.get_value() == value:
            print_error(f"Node with value {value} cannot join,"
                        " because a node with same value is already connected.")
            return False

        joiner: NodeRef = NodeRef(value)
        self.__ooc.ooc_memorize(joiner)

        successor_successor: NodeRef = successor.get_successor()

        # check if it is a single-node-ring
        if successor_successor == successor:
            joiner.set_successors(successor, joiner)
            successor.set_successors(joiner, successor)
            return True

        # otherwise we also find the predecessors and notify them
        predecessor: NodeRef = self.__find_preceding_node(successor)
        predecessor_next: NodeRef = self.__find_preceding_node(predecessor, successor)

        joiner.set_successors(successor, successor_successor)
        predecessor.set_successors(joiner, successor)
        predecessor_next.set_successors(predecessor, joiner)

        return True


    def leave(self, value: int) -> bool:
        """
            We simply terminate the node, silently disconnecting it from the ring,
        without notifying any of the successors.

            Since we need to get precise results for other commands,
        we do the ring-wide refresh right after the leaving, although without the context which
        node left. Initially we were thinking of doing refreshes every time a node notices that
        successor or next successor is not responding to pings, but for example in lookup, we
        discovered it would lead to incorrect lookup request counts.

            To illustrate the last point, consider for example the initial ring from Input-file.txt.
        Assume we have removed node 92 and we are performing lookup to key 90 starting from node 5
        before the leaving is noticed. We would get the wrong lookup request count, unless we lie
        about the request count after doing the requests and finding out that the starting node had
        the key. At the start of the lookup node 5 has keys in range [93, 5], but has [90, 5] once
        node 89 notices unresponsive node 92 and performs a refresh.

        :param value: leaving node value.
        :return: whether leaving was successful or not.
        """

        if value not in self.__ooc:
            print_warning(f"Node with value {value} cannot leave,"
                          " because it has not even joined the ring.")
            return False

        if len(self.__ooc) == 1:
            print_error(f"Node with value {value} cannot leave,"
                        " because less than one node would remain.")
            return False

        self.__ooc.terminate_node(value)
        self.__refresh()

        return True


    def __refresh(self):
        """ Here we perform a ring-wide refresh. """
        starting_node: NodeRef = self.__get_local_node()
        current_node: NodeRef = starting_node

        while True:
            current_node.refresh()
            current_node = current_node.get_successor()

            if current_node == starting_node:
                return


    def add_shortcut(self, start: int, end: int) -> bool:
        """
        First we find the starting and ending node by looking up their values as keys.
        We could have directly created a node reference from the values, but the task instructions
        are not clear about whether we can do that or not. Therefore we did not assume this an
        option and we just do some extra work here.

        Once we have the references, we can just notify the starting node of the new shortcut.

        :param start: starting node value of the shortcut.
        :param end: ending node value of the shortcut.
        :return: whether adding the shortcut was successful or not.
        """

        for word, value in [("start", start), ("end", end)]:
            if not self.__is_in_key_space(value):
                print_error(f"Shortcut {word} node with value {value} is outside of the key-space.")
                return False

        start_node: NodeRef = self.__perform_lookup(start)[0]
        if start_node.get_value() != start:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        " because start node is not in the network.")
            return False

        end_node: NodeRef = self.__perform_lookup(end)[0]
        if end_node.get_value() != end:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        " because end node is not in the network.")
            return False

        if start == end:
            print_warning(f"Shortcut from node {start} to node {end} has the same start and end."
                          " Start node will probably discard this shortcut.")

        result = start_node.add_shortcut(end_node)

        if not result:
            print_error(f"The shortcut might already exist or is a self-loop.")

        return result
