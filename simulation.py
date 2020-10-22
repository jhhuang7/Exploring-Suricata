#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import Link, TCLink, Intf
from mininet.node import RemoteController, Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class FragmentTopo( Topo ):
	def build ( self, **_opts ):
		# Add hosts and switches
		attackerHost = self.addHost( 'h1' )
		targetHost = self.addHost( 'h2' )
		suricataHost = self.addHost( 'h3' )
		legitHost = self.addHost( 'h4' )
		switchEx = self.addSwitch( 's1' )
		switchIn = self.addSwitch( 's2' )

        # Add links
		self.addLink( attackerHost, switchEx)
		self.addLink( legitHost, switchEx)
		self.addLink( targetHost, switchIn)
		self.addLink( suricataHost, switchIn)
		self.addLink( switchEx, switchIn)

		c0 = self.addController("c0", controller=Controller)

        switchIn.start([c0])
    
    	switchIn.cmd("ovs-vsctl del-port s2-eth2")
    	switchIn.cmd("ovs-vsctl add-port s2 s2-eth2 -- --id=@p get port s2-eth2 -- \
			--id=@m create mirror name=m0 select-all=true output-port=@p -- \
			set bridge s1 mirrors=@m")
		

class DdosTopo( Topo ):
	def build ( self, **_opts ):
		attackerHost1 = self.addHost( 'h1' )
		attackerHost2 = self.addHost( 'h5' )
		attackerHost3 = self.addHost( 'h6' )
		attackerHost4 = self.addHost( 'h7' )
		targetHost = self.addHost( 'h2' )
		suricataHost = self.addHost( 'h3' )
		legitHost = self.addHost( 'h4' )
		switchEx1 = self.addSwitch( 's1' )
		switchEx2 = self.addSwitch( 's3' )
		switchEx3 = self.addSwitch( 's4' )
		switchEx4 = self.addSwitch( 's5' )
		switchEx5 = self.addSwitch( 's6' )
		switchIn5 = self.addSwitch( 's2' )

        # Add links
		self.addLink( attackerHost, switchEx1 )
		self.addLink( attackerHost, switchEx2 )
		self.addLink( attackerHost, switchEx3 )
		self.addLink( attackerHost, switchEx4 )
		self.addLink( legitHost, switchEx5 )
		self.addLink( targetHost, switchIn )
		self.addLink( suricataHost, switchIn )
		self.addLink( switchEx1, switchIn )
		self.addLink( switchEx2, switchIn )
		self.addLink( switchEx3, switchIn )
		self.addLink( switchEx4, switchIn )
		self.addLink( switchEx5, switchIn )

def http_test( self, line):
	"Custom CLI command to setup and test HTTP server"

	x = line.split()

	net = self.mn

	
	net.get('h2').cmd('python -m SimpleHTTPServer 8000 &')

	time.sleep(1)

	net.get('h1').cmd("hping3 10.0.0.2 -S -d 120 -p 8000 -q --flood")
	#net.get('h5').cmd("hping3 10.0.0.2 -S -d 120 -p 8000 -q --flood")
	#net.get('h6').cmd("hping3 10.0.0.2 -S -d 120 -p 8000 -q --flood")
	#net.get('h7').cmd("hping3 10.0.0.2 -S -d 120 -p 8000 -q --flood")

	while(1)

		result = net.get('h4').cmd('curl 10.0.0.2:8000')

		print (result)

def fragment_test( self, line):
	net = self.mn

	for i in range(10):

		result = net.get('h1').cmd("ping 10.0.0.2 -c 1")

		print result

	result = net.get('h4').cmd("hping3 10.0.0.2 -C -d 2000 -V --flood")

	print result

	while (1):

		result = net.get('h1').cmd("ping 10.0.0.2 -c 1")

		print result

	


def run():
	topo = FragmentTopo()
	net = Mininet( topo=topo )
	net.start()
	CLI.do_http_test = http_test
	CLI.do_fragment_test = fragment_test
	CLI( net )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	run()