from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink, Intf
from mininet.node import RemoteController, Controller


if '__main__' == __name__:
	net = Mininet(link = TCLink)
	
	topos = ["simple", "mesh", "tree"]
	mode = 0 # Change this ranging from 0 to 2
	topo = topos[mode]
	
	if topo == "simple":
		h1 = net.addHost('h1')
		h2 = net.addHost('h2')
		h3 = net.addHost('h3')
		s1 = net.addSwitch('s1')

		net.addLink(h1, s1)
		net.addLink(h2, s1)
		net.addLink(h3, s1)
	"""
	elif topo == "mesh":
		# Set up mesh topology
	"""
	elif topo == "tree":
		h1 = net.addHost('h1')
		h2 = net.addHost('h2')
		h3 = net.addHost('h3')
		s1 = net.addSwitch('s1')
		s2 = net.addSwitch('s2')
		s3 = net.addSwitch('s3')
		s4 = net.addSwitch('s4')
		s5 = net.addSwitch('s5')

		net.addLink(s2, s1)
		net.addLink(s5, s1)
		net.addLink(s3, s2)
		net.addLink(s4, s2)
		net.addLink(h1, s3)
		net.addLink(h2, s5)
		net.addLink(h3, s1)
	
	c0 = net.addController('c0', controller=Controller)
	Intf('eth1', node =h3)
	net.build()
	c0.start()
	s1.start([c0])
	CLI(net)
	net.stop();

