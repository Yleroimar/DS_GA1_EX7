import multiprocessing as mp

from src.distributed.node_ref import NodeRef
from src.distributed.node import init_node


def start_node_process(reference: NodeRef) -> mp.Process:
    process = mp.Process(target=init_node, args=(reference,),
                         name=f"Process<{reference.get_address()}>")
    process.start()
    return process
