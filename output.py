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
sock.bind(server_address)
sock.listen(1)
conn,addr = sock.accept()

wlist = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"}
blist = {}
hardTimeOut = 20

while True:
	line = conn.recv(10000).decode("utf-8")
	try:
		lines =  line.split('\n')
		for i in lines:
			try:
				if (i == '') :
					continue
				parsed = json.loads(i)

				if (parsed['proto'] == u'TCP'):
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
						os.system("sudo ovs-ofctl add-flow s1 hard_timeout=60,dl_type=0x0800,nw_src="+str(srcIP)+",actions=drop")
						blist[srcIP] = date

			except Exception as e:
				print(e)
				continue

	except Exception as e:
		print(e)
		continue

sock.close()

