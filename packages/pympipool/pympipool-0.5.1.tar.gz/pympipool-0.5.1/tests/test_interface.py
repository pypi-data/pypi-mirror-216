import numpy as np
import unittest
from pympipool.share.communication import SocketInterface
from pympipool.share.serial import get_parallel_subprocess_command, cloudpickle_register


def calc(i):
    return np.array(i ** 2)


class TestInterface(unittest.TestCase):
    def test_interface(self):
        cloudpickle_register(ind=1)
        task_dict = {"fn": calc, 'args': (), "kwargs": {"i": 2}}
        interface = SocketInterface()
        interface.bootup(
            command_lst=get_parallel_subprocess_command(
                port_selected=interface.bind_to_random_port(),
                cores=1,
                cores_per_task=1,
                oversubscribe=False,
                enable_flux_backend=False,
                enable_mpi4py_backend=False,
            )
        )
        self.assertEqual(interface.send_and_receive_dict(input_dict=task_dict), np.array(4))
        interface.shutdown(wait=True)