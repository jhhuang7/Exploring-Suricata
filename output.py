import socket
import sys
import datetime
import os
import json

os.system("sudo ovs-ofctl del-flows s1")


os.system("rm eve.sock")

server_address = "eve.sock"
sock =  socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address);
sock.listen(1)

conn,addr =  sock.accept()

lastA = None
dosProtection = False
# sourceIp = str(parsed['src_ip'])
# destIp = str(parsed['dest_ip'])
# os.system("sudo ovs-ofctl del-flows s1 nw_src="+sourceIp)
# os.system("sudo ovs-ofctl add-flow s1 priority=65535,hard_timeout=300,nw_src="+sourceIp+",actions=drop")

wlist = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5","10.0.0.6"}
blist = {}
hardTimeOut = 60;
ingressPort = {'s1' : [1, 3]};
outFacingSwitches = ['s1'];


def reflectedSpoofProtection():
	for switch in outFacingSwitches:
		for port in ingressPort[switch]:
			for key in wlist:
				a = "sudo ovs-ofctl add-flow "+switch+" hard_timeout=0,in_port="+str(port)+",dl_type=0x0800,nw_src="+str(key)+",actions=drop"
				os.system(a)

reflectedSpoofProtection()
while True:
	line = conn.recv(1000).decode("utf-8")
	try:
		lines =  line.split('\n')
		for i in lines:
			try:
				if (i == '') :
					continue
				parsed = json.loads(i)

				if (parsed['proto'] == u'ICMP') or parsed['proto'] == u'TCP':
					srcIP = parsed['src_ip']
					print(parsed["timestamp"])
					date = datetime.datetime.strptime(parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
					if (srcIP in blist) :
						diff = date - blist[srcIP]
						if diff.total_seconds() >= hardTimeOut:
							del blist[srcIP]
						else:
							continue

					if srcIP not in wlist :
						os.system("sudo ovs-ofctl del-flows s1")
						reflectedSpoofProtection()
						blist[srcIP] = date
						for key in blist:
							os.system("sudo ovs-ofctl add-flow s1 hard_timeout=60,dl_type=0x0800,nw_src="+str(key)+",actions=drop")
						
						# print('------------------------')
						# print('Current Flow Table for s1')
						# os.system("sudo ovs-ofctl dump-flows s1")
					

			except Exception as e:
				continue
	except Exception as e:
		print(e)
		continue

sock.close()

