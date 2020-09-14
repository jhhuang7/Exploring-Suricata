from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink, Intf
from mininet.node import RemoteController, Controller





if '__main__' == __name__:
	net = Mininet(link = TCLink)
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	h3 = net.addHost('h3')
	s1 = net.addSwitch('s1')
	


	c0 = net.addController('c0', controller=Controller)
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	Intf('eth1', node =h3)
	net.build()
	c0.start()
	s1.start([c0])
	CLI(net)
	net.stop();
