from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller
import sys

if '__main__' == __name__:
	net = Mininet(link=TCLink)
	
	
	switches = []
	
	# h1, h7  are "external to the system"
	# h3 and h8 are meant for suricata, for s1 and s5 
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
	h10  = net.addHost('h10')
	
	h11  = net.addHost('h11')
	h12  = net.addHost('h12')

	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')
	s6 = net.addSwitch('s6')
	s7 = net.addSwitch('s7')
	
	switches.append(s1)
	switches.append(s2)
	switches.append(s3)
	switches.append(s4)
	switches.append(s5)
	switches.append(s6)
	switches.append(s7)

	net.addLink(h1, s1) #, bw=3
	net.addLink(h3, s1) #, bw=3
	net.addLink(s1, s2) #, bw=3

	net.addLink(s2, s3) #, bw=3	
	net.addLink(s2, s4) #, bw=3	

	net.addLink(s3, h2) #, bw=3
	net.addLink(s3, h5) #, bw=3

	net.addLink(s4, h4) #, bw=3
	net.addLink(s4, h6) #, bw=3


	net.addLink(s5, s2) #, bw=3
	net.addLink(h7, s5) #, bw=3
	net.addLink(h8, s5) #, bw=3

	net.addLink(s6, s2) #, bw=3
	net.addLink(h9, s6) #, bw=3
	net.addLink(h10, s6) #, bw=3

	net.addLink(s7, s2) #, bw=3
	net.addLink(h11, s7) #, bw=3
	net.addLink(h12, s7) #, bw=3

	if (len(sys.argv) == 1):
		c0 = net.addController('c0', controller=Controller)
	else :
		# any second argument runs it in onos mode
		print(len(sys.argv))
		c0 = net.addController('c0', controller=RemoteController)

	for s in switches:
		s.start([c0])

	net.build()
	c0.start()
	
	x = CLI(net)
	net.stop()
