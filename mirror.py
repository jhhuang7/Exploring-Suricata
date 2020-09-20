from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller


if '__main__' == __name__:
	net = Mininet(link=TCLink)
	
	topos = ["simple", "mesh", "tree"]  # May add most hosts and switches for more complexity for each topo
	mode = 2  # Change this ranging from 0 to 2
	topo = topos[mode]
	
	hosts = 0
	switches = 0
	
	if topo == "simple":
		h1 = net.addHost('h1')
		h2 = net.addHost('h2')
		h3 = net.addHost('h3')
		s1 = net.addSwitch('s1')

		net.addLink(h1, s1)
		net.addLink(h2, s1)
		net.addLink(h3, s1)
		
		hosts = 3
		switches = 1
		
	elif topo == "mesh":
		h1 = net.addHost('h1')
		h2 = net.addHost('h2')
		h3 = net.addHost('h3')
		s1 = net.addSwitch('s1')
		s2 = net.addSwitch('s2')
		s3 = net.addSwitch('s3')
		s4 = net.addSwitch('s4')
		
		net.addLink(s2, s1)
		net.addLink(s3, s1)
		net.addLink(s4, s1)
		net.addLink(s3, s2)
		net.addLink(s4, s2)
		net.addLink(s3, s4)
		net.addLink(h1, s1)
		net.addLink(h1, s1)
		net.addLink(h2, s3)
		net.addLink(h3, s1)
		
		hosts = 3
		switches = 4
		
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
		
		hosts = 3
		switches = 5
	
	c0 = net.addController('c0', controller=Controller)
	Intf('eth1', node=h3)  # May need to change 'eth' depending on the VM's internet connection
	net.build()
	c0.start()
	
	s1.start([c0])
	if switches >= 4:
		s2.start([c0])
		s3.start([c0])
		s4.start([c0])
	if switches >= 5:
		s5.start([c0])
	
	CLI(net)
	net.stop();
