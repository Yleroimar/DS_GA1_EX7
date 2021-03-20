import multiprocessing as mp

from utils.distributed.node_ref import NodeRef
from utils.distributed.node import init_node


def start_node_process(reference: NodeRef) -> mp.Process:
    process = mp.Process(target=init_node, args=(reference,),
                         name=f"Process<{reference.host}:{reference.port}>")
    process.start()
    return process
