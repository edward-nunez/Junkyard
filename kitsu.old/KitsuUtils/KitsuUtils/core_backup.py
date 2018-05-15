""" Implements wrappers for underlying OS control and interaction

    Todo:
        * Add additional function wrappers as needed
        * Add more Windows support
"""

from multiprocessing import Pool, Process, Queue, current_process, freeze_support, cpu_count, Manager
import os
import platform
import subprocess


FNULL = open(os.devnull, 'w')

def ping(node):

    """ Pings the specified host to check connectivity

        Args:
            node (string): hostname or IPv4 address of target node

        Returns:
            bool: Whether the ping succeeded or not
    """

    countstr = "-n 1" if platform.system().lower() == 'windows' else '-c 1'
    cmd = 'ping {c} {n}'.format(c=countstr, n=node)
    return subprocess.call(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT) == 0

def is_reachable(node):

    """ More intuitive wrapper for checking reachability of node

        Args:
            node (string): node to check status of

        Returns:
            bool: Whether the node can be reached
    """
    
    return ping(node)

def _map_worker((func, args)):

    """ Worker function for use with p_execute

        Args:
            tuple(func, args): 
                func (function ptr): function to be executed
                args (tuple): arguments to be passed to func

    """

    result = func(*args)
    return result

def p_execute(work_list, print_output=True):

    output_list = []
    for result in Pool().imap(_map_worker, work_list):
        if print_output:
            print result
        
        output_list.append(result)
    
    return output_list
