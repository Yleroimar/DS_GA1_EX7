import xmlrpc.client
from functools import total_ordering
from typing import Any, Callable, TypeVar, Tuple

from utils.constants import LOCALHOST


def address_mapper(key: int) -> (str, int):
    return LOCALHOST, 8000 + key


value_to_address_mapper: Callable[[int], Tuple[str, int]] = address_mapper

NodeRef = 'NodeRef'
T = TypeVar('T')


@total_ordering
class NodeRef:
    def __init__(self, value: int):
        self.value: int = value


    def __init_proxy(self) -> xmlrpc.client.ServerProxy:
        return xmlrpc.client.ServerProxy(f"http://{self.get_host()}:{self.get_port()}/")


    def apply_to_proxy(self, proxy_func: Callable[[xmlrpc.client.ServerProxy], T]) -> T:
        with self.__init_proxy() as proxy:
            return proxy_func(proxy)


    def get_value(self) -> int:
        return self.value


    def get_host(self) -> str:
        return value_to_address_mapper(self.value)[0]


    def get_port(self) -> int:
        return value_to_address_mapper(self.value)[1]


    def get_address(self) -> (str, int):
        return value_to_address_mapper(self.value)


    def get_keys_start(self) -> int:
        return self.apply_to_proxy(lambda proxy: proxy.get_keys_start())


    def get_successor(self) -> NodeRef:
        return unmarshall_node_ref(self.apply_to_proxy(lambda proxy: proxy.get_successor()))


    def get_successor_next(self) -> NodeRef:
        return unmarshall_node_ref(self.apply_to_proxy(lambda proxy: proxy.get_successor_next()))


    def set_successors(self, successor: NodeRef, successor_next: NodeRef):
        self.apply_to_proxy(lambda proxy: proxy.set_successors(successor, successor_next))


    def notify_of_preceding(self, predecessor: NodeRef):
        self.apply_to_proxy(lambda proxy: proxy.notice_from_predecessor(predecessor))


    def ask_lookup_direction(self, target_key: int) -> NodeRef:
        return unmarshall_node_ref(self.apply_to_proxy(
            lambda proxy: proxy.ask_lookup_direction(target_key)
        ))


    def refresh(self):
        self.apply_to_proxy(lambda proxy: proxy.refresh())


    def is_alive(self) -> bool:
        try:
            with self.__init_proxy() as proxy:
                return proxy.ping()
        except OSError:
            return False


    def add_shortcut(self, target: NodeRef) -> bool:
        return self.apply_to_proxy(lambda proxy: proxy.add_shortcut(target))


    def __contains__(self, item: Any) -> bool:
        return self.apply_to_proxy(lambda proxy: proxy.contains(item))


    def __str__(self) -> str:
        return self.apply_to_proxy(lambda proxy: proxy.to_string())


    def __repr__(self) -> str:
        return self.apply_to_proxy(lambda proxy: proxy.to_string())


    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NodeRef) and self.get_address() == other.get_address()


    def __lt__(self, other: Any):
        return isinstance(other, NodeRef) and self.value < other.value


    def __hash__(self):
        return hash(self.get_address())


def unmarshall_node_ref(marshalled: dict or NodeRef) -> NodeRef:
    return NodeRef(**marshalled) if type(marshalled) == dict else marshalled
