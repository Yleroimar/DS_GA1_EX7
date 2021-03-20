from typing import Any
from xmlrpc.server import SimpleXMLRPCServer

from utils.constants import IS_DEBUGGING
from utils.distributed.node_ref import NodeRef, unmarshall_ref


class Node:
    """
    Nodes act as peers in the ring.

    The nodes mostly just form the structure of the ring and hold the keys (and irl also data).
    The nodes have very little other functionality attached to them. Other functionality includes
    local-refreshing of references to successors and giving directions on lookup.

    In order to prevent deadlocks and blocking of the ring, recursive requests are not used.
    """


    def __init__(self, reference: NodeRef):
        self.__reference: NodeRef = reference

        self.__successor: NodeRef = self.__reference
        self.__successor_next: NodeRef = self.__reference

        self.__keys_start: int = self.__set_keys_start(self.__reference)

        self.__finger_table: [NodeRef] = []


    def get_value(self) -> int:
        return self.__reference.get_value()


    def get_keys_start(self) -> int:
        return self.__keys_start


    def get_successor(self) -> NodeRef:
        return self.__successor


    def get_successor_next(self) -> NodeRef:
        return self.__successor_next


    def set_successors(self, successor: NodeRef or dict, successor_next: NodeRef or dict):
        self.set_successor(successor)
        self.set_successor_next(successor_next)


    def set_successor(self, successor: NodeRef or dict):
        self.__set_successor(unmarshall_ref(successor))


    def set_successor_next(self, successor_next: NodeRef or dict):
        self.__set_successor_next(unmarshall_ref(successor_next))


    def __set_successor(self, successor: NodeRef):
        self.__successor = successor
        self.__notify_successor(successor)


    def __set_successor_next(self, successor_next: NodeRef):
        self.__successor_next = successor_next


    def __notify_successor(self, successor: NodeRef):
        if self.is_self(successor):
            self.__set_keys_start(successor)
        else:
            successor.notify_of_preceding(self.__reference)


    def notice_from_predecessor(self, predecessor: NodeRef or dict):
        self.__set_keys_start(unmarshall_ref(predecessor))


    def notice_from_successor(self, successor: NodeRef or dict):
        self.__successor = unmarshall_ref(successor)


    def notice_from_successor_next(self, successor_next: NodeRef or dict):
        self.__successor_next = unmarshall_ref(successor_next)


    def __set_keys_start(self, predecessor: NodeRef) -> int:
        self.__keys_start = predecessor.get_value() + 1
        return self.__keys_start


    def ask_lookup_direction(self, target_key: int) -> NodeRef:
        """
        First we check if the node has the key.
        Then we check if any of the fingers have the key or if they get us closer to the target key.
        Finally we pass the successor node as the next node to look up.

        :param target_key: key value that is being searched for.
        :return: reference to self if the key is here, otherwise next node to look up.
        """

        if target_key in self:
            return self.__reference

        value: int = self.get_value()

        descending_fingers: [NodeRef] = sorted(self.__finger_table)[::-1]

        for finger in descending_fingers:
            # check if fingers have the value or if fingers get us closer, in which case we require
            #  that target_key is bigger than finger
            #  and that current node is smaller or bigger than both
            finger_value = finger.get_value()
            if (target_key in finger
                    or finger_value <= target_key
                    and (value < finger_value or target_key < value)):
                return finger

        # check if the highest finger gets us closer if the target key is smaller than current value
        if target_key < value and 0 < len(descending_fingers):
            highest_finger: NodeRef = descending_fingers[0]
            if self.__reference < highest_finger:
                return highest_finger

        return self.__successor


    def is_self(self, node: NodeRef) -> bool:
        return self.__reference == node


    def is_single_node_ring(self) -> bool:
        return self.is_self(self.get_successor())


    def refresh(self):
        self.__finger_table: [NodeRef] = [finger
                                          for finger in self.__finger_table
                                          if finger.is_alive()]

        self.__refresh_successors_references()


    def __refresh_successors_references(self):
        # single-node-ring
        if self.is_single_node_ring():
            return

        if not self.__successor.is_alive():
            self.set_successor(self.get_successor_next())

            if not self.is_single_node_ring():
                self.set_successor_next(self.get_successor().get_successor())

            return

        successor: NodeRef = self.get_successor()
        if not self.is_self(self.get_successor_next()) and not self.get_successor_next().is_alive():
            successor_next: NodeRef = successor.get_successor()

            # check if successor has already been updated
            if successor_next == self.get_successor_next():
                successor_next = successor.get_successor_next()

            self.set_successor_next(successor_next)


    @staticmethod
    def ping() -> True:
        return True


    def add_shortcut(self, target: NodeRef or dict) -> bool:
        return self.__add_shortcut(unmarshall_ref(target))


    def __add_shortcut(self, target: NodeRef) -> bool:
        if self.is_self(target):
            return False

        if target in self.__finger_table:
            return False

        self.__finger_table.append(target)
        return True


    def contains(self, item: Any) -> bool:
        return item in self


    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, int):
            return False

        keys_end: int = self.get_value()
        keys_start: int = self.__keys_start

        return (keys_start <= item <= keys_end  # trivial check
                # if key range is cross-seam (if start is bigger than end)
                # then check if the key is outside of key range (is strictly between end and start)
                or keys_end < keys_start and not keys_end < item < keys_start)


    def to_string(self) -> str:
        return str(self)


    def __str__(self) -> str:
        return self.__repr__()


    def __repr__(self) -> str:
        shortcuts: str = ",".join(str(node.get_value()) for node in sorted(self.__finger_table))

        return f"{self.get_value()}:{shortcuts}," \
               f" S-{self.get_successor().get_value()}," \
               f" NS-{self.get_successor_next().get_value()}"


def init_node(reference: NodeRef):
    node: Node = Node(reference)

    with SimpleXMLRPCServer((reference.get_host(), reference.get_port()),
                            allow_none=True, logRequests=IS_DEBUGGING) as server:
        server.register_instance(node)
        server.serve_forever()
        print(f"{reference} closing.")
