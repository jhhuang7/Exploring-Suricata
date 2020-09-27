import sys
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller

"""
Script to build a custom tree topology in mininet given number of hosts.
"""

def build_tree(num_hosts: int):
    net = Mininet(link=TCLink)

    switches = []
    
    # Build up the tree network topology with hosts, switches and links
    # based on the given number of hosts. Tree is going to be a binary tree.

    c0 = net.addController("c0", controller=Controller)
	
    for switch in switches:
        switch.start([c0])
    
    s1.cmd("ovs-vsctl del-port s1-eth2")
    s1.cmd("ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- \
        --id=@m create mirror name=m0 select-all=true output-port=@p -- \
        set bridge s1 mirrors=@m")
    
    net.build()
    c0.start()
    
    x = CLI(net)
    net.stop()


def main(args):
    if len(args) != 1:
        print("Requires one argument of num_hosts (int).")
        return

    try:
        num_hosts = int(args[0])
    except ValueError:
        print("Number of hosts must be an int.")
        return

    build_tree(num_hosts)


if __name__ == "__main__":
    # Takes in one command line argument of number of hosts
    main(sys.argv[1:])
