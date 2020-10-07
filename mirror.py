from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller


if '__main__' == __name__:
	net = Mininet(link=TCLink)
	
	switches = []
	
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	h3 = net.addHost('h3')
	h4  = net.addHost('h4')
	h5  = net.addHost('h5')
	h6  = net.addHost('h6')
	h7  = net.addHost('h7')

	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	
	switches.append(s1)
	switches.append(s2)
	switches.append(s3)
	switches.append(s4)

	net.addLink(h1, s1)
	net.addLink(h3, s1)
	net.addLink(h7, s1)

	net.addLink(s1, s2)
	net.addLink(s2, s3)	
	net.addLink(s2, s4)	

	net.addLink(s3, h2)
	net.addLink(s3, h5)

	net.addLink(s4, h4)
	net.addLink(s4, h6)


	c0 = net.addController('c0', controller=Controller)
	
	for s in switches:
		s.start([c0])

	s1.cmd('ovs-vsctl del-port s1-eth2')
	s1.cmd('ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m')

	
	net.build()
	c0.start()
	
	x = CLI(net)
	net.stop()
