from ds_hw1_dht_node import Node
from ds_hw1_dht_printing import print_error, print_warning


class Ring:
    def __init__(self, ks_start: int, ks_end: int, node_values: [int], shortcuts: [(int, int)]):
        self.ks_start: int = ks_start
        self.ks_end: int = ks_end

        self.nodes: {int: Node} = self.create_nodes_and_assign_successors(node_values)

        self.add_shortcuts(shortcuts)

    def create_nodes_and_assign_successors(self, node_values: [int]) -> [Node]:
        nodes: [Node] = [Node(value, self.ks_start, self.ks_end) for value in sorted(node_values)]

        for node, successor, successor2 in zip(nodes, nodes[1:] + nodes[:1], nodes[2:] + nodes[:2]):
            node.set_successors(successor, successor2)

        return dict((node.value, node) for node in nodes)

    def add_shortcuts(self, shortcuts: (int, int)):
        for start, end in shortcuts:
            self.add_shortcut(start, end)

    def add_shortcut(self, start: int, end: int):
        self.nodes[start].add_shortcut_to(self.nodes[end])

    def list_as_str(self) -> str:
        return "\n".join(str(node)
                         for _, node in sorted(self.nodes.items(), key=lambda pair: pair[0]))

    def lookup(self, target_key: int, starting_value: int or None = None) -> (int, int) or None:
        if not self.ks_start <= target_key <= self.ks_end:
            print_error(f"Lookup key {target_key} is outside of key-space!")
            return None

        if starting_value is None:
            starting_value = min(self.nodes.keys())

        return self.nodes[starting_value].lookup(target_key)

    def find_preceding_node(self, node: Node) -> Node:
        nodes_sorted: [Node] = [r for _, r in sorted(self.nodes.items(), key=lambda pair: pair[0])]

        previous: Node = nodes_sorted[-1]
        while True:
            successor: Node = previous.successor

            if node.value <= successor.value:
                break

            previous = successor

        return previous

    def find_proceeding_node(self, node: Node) -> Node:
        proceeding_node = self.find_preceding_node(node).successor
        return proceeding_node.successor if node == proceeding_node else proceeding_node

    def find_predecessors(self, node: Node) -> (Node, Node):
        """
        :param node: successor of the returned predecessors. Can be absent from the ring.
        :return: the non-leaving next predecessor and predecessor. Skips predecessors until found.
        """
        predecessor = self.find_preceding_node(node)
        while predecessor.is_leaving:
            predecessor = self.find_preceding_node(predecessor)

        predecessor_next = self.find_preceding_node(predecessor)
        while predecessor_next.is_leaving:
            predecessor_next = self.find_preceding_node(predecessor_next)

        return predecessor_next, predecessor

    def find_successors(self, node: Node) -> (Node, Node):
        """
        :param node: predecessor of the returned successors. Can be absent from the ring.
        :return: the non-leaving successor and next successor. Skips successors until found.
        """
        successor = self.find_proceeding_node(node)
        while successor.is_leaving:
            successor = successor.successor

        successor_next = successor.successor
        while successor_next.is_leaving:
            successor_next = successor_next.successor

        return successor, successor_next

    def join(self, node_value: int):
        if not self.ks_start <= node_value <= self.ks_end:
            print_warning(f"Node with value {node_value} cannot join,"
                          f" because it is outside of the key-space.")
            return

        if node_value in self.nodes:
            print_warning(f"Node with value {node_value} cannot join,"
                          f" because it has already joined.")
            return

        new_node = Node(node_value, self.ks_start, self.ks_end)

        self.nodes[node_value] = new_node

        successor, successor_next = self.find_successors(new_node)
        predecessor_next, predecessor = self.find_predecessors(new_node)

        new_node.set_successors(successor, successor_next)
        predecessor.set_successors(new_node, successor)
        predecessor_next.set_successors(predecessor, new_node)

    def leave(self, node_values: [int]):
        """ Covers both the case where a single node leaves and where multiple nodes leave. """
        nodes_leaving = []

        for node_value in node_values:
            if node_value not in self.nodes:
                print_warning(f"Node with value {node_value} has already left or is leaving twice.")
                continue

            nodes_leaving.append(node := self.nodes[node_value])
            node.prepare_to_leave()
            self.nodes.pop(node_value)

        for node in nodes_leaving:
            successor, successor_next = self.find_successors(node)

            if node == successor_next:
                successor.set_successors(successor, successor)
                self.remove_shortcuts_to(node)
                continue

            predecessor_next, predecessor = self.find_predecessors(node)

            predecessor_next.set_successors(predecessor, successor)
            predecessor.set_successors(successor, successor_next)

            self.remove_shortcuts_to(node)

    def remove_shortcuts_to(self, node: Node):
        for from_node in self.nodes.values():
            finger_table = from_node.finger_table

            if node in finger_table:
                finger_table.remove(node)
