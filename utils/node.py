class Node:
    def __init__(self, value: int, ks_min: int, ks_max: int):
        self.value: int = value
        self.is_leaving: bool = False

        self.ks_min: int = ks_min
        self.ks_max: int = ks_max

        self.successor: Node = self
        self.successor_next: Node = self

        self.keys_start: int = self.set_keys_start(self)

        self.finger_table: [Node] = []

    def prepare_to_leave(self):
        self.is_leaving = True

    def set_keys_start(self, predecessor) -> int:
        self.keys_start = predecessor.value + 1

        if self.ks_max < self.keys_start:
            self.keys_start = self.ks_min

        return self.keys_start

    def get_keys(self) -> [int]:
        if self.keys_start < self.value:
            return list(range(self.keys_start, self.value + 1))

        keys = (list(range(self.keys_start, self.ks_max + 1))
                + list(range(self.ks_min, self.value + 1)))

        if self.keys_start == self.value:
            return keys[1:]  # to avoid the first and last element being the same

        return keys

    def set_successors(self, successor, successor_next):
        self.set_successor(successor)
        self.set_successor_next(successor_next)

    def set_successor(self, successor):
        self.successor = successor
        successor.set_keys_start(self)

    def set_successor_next(self, successor_next):
        self.successor_next = successor_next

    def add_shortcut_to(self, node):
        self.finger_table.append(node)

    def lookup(self, target_key: int, n_requests: int = 0) -> (int, int):
        if target_key in self.get_keys():
            return self.value, n_requests

        for node in sorted(self.finger_table, key=lambda x: x.value)[::-1]:
            if node.value <= target_key:
                return node.lookup(target_key, n_requests + 1)

        return self.successor.lookup(target_key, n_requests + 1)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        shortcuts = ",".join(str(node.value) for node in self.finger_table)
        return f"{self.value}:{shortcuts}, S-{self.successor.value}, NS-{self.successor_next.value}"
