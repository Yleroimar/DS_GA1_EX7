from functools import total_ordering
from typing import Any

from utils.printing import print_warning, print_error


Node = 'Node'


@total_ordering
class Node:
    """ Implements the peer in the DHT ring network. """

    def __init__(self, value: int):
        self.__value: int = value

        self.__successor: Node = self
        self.__successor_next: Node = self

        self.__alive: bool = True

        self.__keys_start: int = self.__set_keys_start(self)

        self.__finger_table: [Node] = []


    def get_value(self) -> int:
        return self.__value


    def get_successor(self) -> Node:
        return self.__successor


    def get_successor_next(self) -> Node:
        return self.__successor_next


    def is_alive(self) -> bool:
        return self.__alive


    def set_successors(self, successor: Node, successor_next: Node):
        self.__set_successor(successor)
        self.__set_successor_next(successor_next)


    def __set_successor(self, successor: Node):
        self.__successor = successor
        successor.__set_keys_start(self)


    def __set_successor_next(self, successor_next: Node):
        self.__successor_next = successor_next


    def __set_keys_start(self, predecessor: Node) -> int:
        self.__keys_start = predecessor.get_value() + 1
        return self.__keys_start


    def add_shortcut_by_value(self, shortcut_end_node_value: int):
        """ Finds the end node of the shortcut, as if we don't have an actual reference to it. """

        node, _ = self.lookup(shortcut_end_node_value)

        if node.get_value() != shortcut_end_node_value:
            print_error("Cannot add shortcut"
                        f" from node {self.get_value()} to node {shortcut_end_node_value},"
                        " because shortcut end node is not present in the network.")
            return

        self.add_shortcut(node)


    def add_shortcut(self, target_node: Node):
        self.__finger_table.append(target_node)


    def list_as_str(self) -> str:
        return str(self) + self.__successor.__list_as_str(self)


    def __list_as_str(self, starter: Node) -> str:
        return (""
                if starter is self
                else (f"\n{str(self)}" + self.__successor.__list_as_str(starter)))


    def lookup(self, target_key: int) -> (Node or None, int):
        return self.__lookup(target_key)


    def __lookup(self, target_key: int, n_requests: int = 0) -> (Node or None, int):
        if target_key in self:
            return self, n_requests

        descending_fingers: [Node] = sorted(self.__finger_table)[::-1]

        for node in descending_fingers:
            if target_key in node or self.get_value() < node.get_value() <= target_key:
                return node.__lookup(target_key, n_requests + 1)

        if target_key < self.get_value() and 0 < len(descending_fingers):
            highest_finger: Node = descending_fingers[0]
            if self < highest_finger:
                return highest_finger.__lookup(target_key, n_requests + 1)

        return self.__successor.__lookup(target_key, n_requests + 1)


    def handle_joiner(self, node_value: int) -> Node or None:
        """
        Handles the joining node by finding a suitable place in the ring for it,
         and then notifying successors to refresh their own successors.
        """
        if self.get_value() == node_value:
            print_warning(f"Node with value {node_value} cannot join,"
                          " because it has already joined.")
            return None

        # is this a single-node ring?
        if self == self.__successor:
            new_node: Node = Node(node_value)

            self.__set_successor(new_node)
            new_node.__set_successor(self)

            return new_node

        successor_value: int = self.__successor.get_value()

        if (self.get_value() < node_value < successor_value
                or self.__successor < self
                and not successor_value <= node_value <= self.get_value()):
            new_node: Node = Node(node_value)

            new_node.__set_successor(self.__successor)
            self.__set_successor(new_node)
            self.refresh()

            return new_node

        return self.__successor.handle_joiner(node_value)


    def leave(self):
        """ Instructions were not clear on if successor is allowed to be notified when leaving. """
        self.__alive = False
        self.__successor = self
        self.__successor_next = self


    def refresh(self):
        """ Refreshes the successors of nodes in the ring. Checks if any successor has left. """
        self.__refresh()


    def __refresh(self, refresh_start: Node or None = None):
        if self is refresh_start:
            return

        self.__finger_table = [node for node in self.__finger_table if node.is_alive()]

        if not self.__successor.is_alive():
            self.__set_successor(self.__find_first_alive_successor())

        self.__successor.__refresh(self if refresh_start is None else refresh_start)

        self.__set_successor_next(self.__successor.get_successor())


    def __find_first_alive_successor(self) -> Node:
        if self.__successor.is_alive():
            return self.__successor

        if self.__successor_next.is_alive():
            return self.__successor_next


    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, int):
            return False

        return (self.__keys_start <= item <= self.__value
                or self.__value < self.__keys_start and not self.__value < item < self.__keys_start)


    def __str__(self) -> str:
        return self.__repr__()


    def __repr__(self) -> str:
        shortcuts: str = ",".join(str(node.get_value()) for node in sorted(self.__finger_table))

        return f"{self.__value}:{shortcuts}," \
               f" S-{self.__successor.__value}," \
               f" NS-{self.__successor_next.__value}"


    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Node) and self.__value == other.__value


    def __lt__(self, other: Any):
        return isinstance(other, Node) and self.__value < other.__value
