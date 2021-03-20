from multiprocessing import Process
from typing import Any, Optional

from utils.distributed.node_process import start_node_process
from utils.distributed.node_ref import NodeRef
from utils.printing import print_warning, print_error_and_stop, print_error


class RingOOC:
    """ Contains the Out-Of-Character (OOC) information and functionality. """


    def __init__(self, ks_bounds: (int, int), node_values: [int], shortcuts: [(int, int)]):
        self.__ks_start, self.__ks_end = ks_bounds

        self.__nodes: {int: NodeRef} = dict()
        self.__processes: {int: Process} or None = dict()
        self.__start_nodes_with_successors(node_values)

        self.__add_shortcuts(shortcuts)


    def __start_nodes_with_successors(self, node_values: [int]):
        valid_values: {int} = set()

        for value in node_values:
            if self.__is_in_key_space(value):
                valid_values.add(value)
            else:
                print_warning(f"Node value {value} is out of key-space! Discarding...")

        if len(valid_values) == 0:
            print_error_and_stop("No (suitable) node values provided!"
                                 " Ring requires at least one node value for initialization!")

        refs: [NodeRef] = [NodeRef(value) for value in sorted(valid_values)]

        for ref in refs:
            self.ooc_memorize(ref)

        for ref, succ, succ_next in zip(refs, refs[1:] + refs[:1], refs[2:] + refs[:2]):
            ref.set_successors(succ, succ_next)


    def __is_in_key_space(self, key: int) -> bool:
        return self.__ks_start <= key <= self.__ks_end


    def __add_shortcuts(self, shortcuts: [(int, int)]):
        for start, end in shortcuts:
            self.__add_shortcut(start, end)


    def __add_shortcut(self, start: int, end: int):
        if start not in self or end not in self:
            print_error(f"Cannot add shortcut from node {start} to node {end},"
                        "because start and/or end node is not in the network.")
            return

        self.__nodes[start].add_shortcut(self.__nodes[end])


    def ooc_memorize(self, node: NodeRef):
        self.__nodes[node.get_value()] = node
        self.__processes[node.get_value()] = start_node_process(node)


    def get_node(self, key: int) -> Optional[NodeRef]:
        return self.__nodes[key] if key in self else None


    def get_lowest_node(self) -> NodeRef:
        return min(self.__nodes.values())


    def get_lowest_node_value(self) -> int:
        return min(self.__nodes.values()).get_value()


    def list_as_str(self) -> str:
        """ OOC version of listing. Only used in testing. """
        return "\n".join(str(node) for node in sorted(self.__nodes.values()))


    def terminate_node(self, node: NodeRef or int):
        node: int = node if isinstance(node, int) else node.get_value()

        self.__nodes.pop(node)
        process: Process = self.__processes.pop(node)
        process.terminate()
        process.join()


    def __contains__(self, item: Any) -> bool:
        return (isinstance(item, NodeRef) and item in self.__nodes.values()
                or isinstance(item, int) and item in self.__nodes.keys())


    def __len__(self):
        return len(self.__nodes)


    def __del__(self):
        """ Performs OOC cleanup. """

        for process in self.__processes.values():
            process.terminate()

        for process in self.__processes.values():
            process.join()
