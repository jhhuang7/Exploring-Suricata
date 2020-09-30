import sys
import math
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller

"""
Script to build a custom tree topology in mininet given number of hosts.
"""

def build_tree(num_hosts: int):
    """
    Build up the tree network topology with hosts, switches and links
    based on the given number of hosts. Tree is going to be a binary tree.
    """

    net = Mininet(link=TCLink)
    topo = [None]  # Element at i = 0 doesn't get used

    level = math.ceil(math.log2(num_hosts))  # level of tree hosts are on
    num_switches = int(sum([math.pow(2, n) for n in range(0, level)]))
    
    # Add switches
    for i in range(0, num_switches):
        name = "s" + str(i + 1)
        switch = net.addSwitch(name)
        topo.append(switch)

    # Add hosts
    for j in range(0, num_hosts):
        name = "h" + str(j + 1)
        host = net.addHost(name)
        topo.append(host)
    
    # Add links
    for k in range(1, len(topo)):
        # Left child
        if 2 * k <= len(topo) - 1:
            net.addLink(topo[k], topo[2 * k])
        
        # Right child
        if 2 * k + 1 <= len(topo) - 1:
            net.addLink(topo[k], topo[2 * k + 1])

    c0 = net.addController("c0", controller=Controller)
    for s in range(1, num_switches + 1):
        topo[s].start([c0])
    
    topo[1].cmd("ovs-vsctl del-port s1-eth2")
    topo[1].cmd("ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- \
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
    
    if num_hosts < 3:
        print("Number of hosts must be greater or equal to 3.")
        return

    build_tree(num_hosts)


if __name__ == "__main__":
    # Takes in one command line argument of number of hosts
    main(sys.argv[1:])
