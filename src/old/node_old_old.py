from functools import total_ordering
from typing import Any


Node = 'Node'


@total_ordering
class Node:
    def __init__(self, value: int, ks_min: int, ks_max: int):
        self.value: int = value
        self.is_leaving: bool = False

        self.__ks_min: int = ks_min
        self.__ks_max: int = ks_max

        self.successor: Node = self
        self.successor_next: Node = self

        self.__keys_start: int = self.__set_keys_start(self)

        self.finger_table: [Node] = []

    def prepare_to_leave(self):
        self.is_leaving = True

    def __set_keys_start(self, predecessor: Node) -> int:
        self.__keys_start = predecessor.value + 1

        if self.__ks_max < self.__keys_start:
            self.__keys_start = self.__ks_min

        return self.__keys_start

    def get_keys(self) -> {int}:
        if self.__keys_start < self.value:
            return set(range(self.__keys_start, self.value + 1))

        return set(list(range(self.__keys_start, self.__ks_max + 1))
                   + list(range(self.__ks_min, self.value + 1)))

    def set_successors(self, successor: Node, successor_next: Node):
        self.__set_successor(successor)
        self.__set_successor_next(successor_next)

    def __set_successor(self, successor: Node):
        self.successor = successor
        successor.__set_keys_start(self)

    def __set_successor_next(self, successor_next: Node):
        self.successor_next = successor_next

    def add_shortcut_to(self, node: Node):
        self.finger_table.append(node)

    def lookup(self, target_key: int, n_requests: int = 0) -> (int, int):
        if target_key in self.get_keys():
            return self.value, n_requests

        for node in sorted(self.finger_table)[::-1]:
            if node.value <= target_key:
                return node.lookup(target_key, n_requests + 1)

        return self.successor.lookup(target_key, n_requests + 1)

    def get_non_leaving_successor(self):
        """ :return: non-leaving successor node, possibly the node itself. """
        successor: Node = self.successor

        while successor is not self and successor.is_leaving:
            successor = successor.successor

        return successor

    def refresh_successors_join(self, new_successor: Node):
        """
        Recursion through all the succeeding nodes, refreshing successors.
        Starts from newly joined node.

        :param new_successor: new successor node, expected to be non-leaving.
        """
        self.__refresh_successors_join(new_successor, starting_node_successor=new_successor)

    def __refresh_successors_join(self, new_successor: Node, starting_node_successor: Node,
                                  starting_node: Node or None = None):
        """
        :param new_successor: new successor node, expected to be non-leaving.
        :param starting_node_successor: is to give incoming references to starting_node
         (recursion starting node).
        :param starting_node: node to mark the start of recursion.
        """
        if starting_node is self:
            return

        if starting_node is None:
            starting_node = self

        self.__set_successor(new_successor)

        new_successor_next: Node = new_successor.get_non_leaving_successor()

        if new_successor_next is starting_node_successor:
            new_successor_next = starting_node
            starting_node_successor = None

        self.__set_successor_next(new_successor_next)

        new_successor.__refresh_successors_join(new_successor_next,
                                                starting_node_successor, starting_node)

    def refresh_refs_leave(self, new_successor: Node):
        """
        Recursion through all the succeeding nodes, refreshing successors and shortcuts.
        Starts from any of the non-leaving nodes.

        :param new_successor: new successor node, expected to be non-leaving.
        """
        self.__refresh_refs_leave(new_successor)

    def __refresh_refs_leave(self, new_successor: Node, starting_node: Node or None = None):
        """
        :param new_successor: new successor node, expected to be non-leaving.
        :param starting_node: node to mark the start of recursion.
        """
        if starting_node is self:
            return

        if starting_node is None:
            starting_node = self

        for shortcut in list(self.finger_table):
            if shortcut.is_leaving:
                self.finger_table.remove(shortcut)

        self.__set_successor(new_successor)

        new_successor_next: Node = new_successor.get_non_leaving_successor()
        self.__set_successor_next(new_successor_next)

        new_successor.__refresh_refs_leave(new_successor_next, starting_node)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        shortcuts: str = ",".join(str(node.value) for node in self.finger_table)
        return f"{self.value}:{shortcuts}, S-{self.successor.value}, NS-{self.successor_next.value}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Node) and self.value == other.value

    def __lt__(self, other: Any):
        return isinstance(other, Node) and self.value < other.value
