from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller


if '__main__' == __name__:
	net = Mininet(link=TCLink)
	
	
	switches = []
	
	# h1, h7 and h9 are "external to the system"
	# h3 and h8 are meant for suricata, for s1 and s5 respectively
	# if suricata is not running  installed that are treated as "external"
	# h2, h4, h5, h6 are treated as internal.to the network.

	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	h3 = net.addHost('h3')
	h4  = net.addHost('h4')
	h5  = net.addHost('h5')
	h6  = net.addHost('h6')
	h7  = net.addHost('h7')
	h8  = net.addHost('h8')
	h9  = net.addHost('h9')

	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')
	
	switches.append(s1)
	switches.append(s2)
	switches.append(s3)
	switches.append(s4)
	switches.append(s5)

	net.addLink(h1, s1)
	net.addLink(h3, s1)
	net.addLink(h9, s1)

	net.addLink(s1, s2)
	net.addLink(s2, s3)	
	net.addLink(s2, s4)	

	net.addLink(s3, h2)
	net.addLink(s3, h5)

	net.addLink(s4, h4)
	net.addLink(s4, h6)


	net.addLink(s5, s2)
	net.addLink(h7, s5)
	net.addLink(h8, s5)

	c0 = net.addController('c0', controller=Controller)
	
	for s in switches:
		s.start([c0])

	net.build()
	c0.start()
	
	x = CLI(net)
	net.stop()
