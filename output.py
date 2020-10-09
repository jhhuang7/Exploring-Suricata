import socket
import sys
import datetime
import os
import json

os.system("sudo ovs-ofctl del-flows s1")
os.system("rm eve.sock")

server_address = "eve.sock"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)
conn,addr = sock.accept()

wlist = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"}
blist = {}
hardTimeOut = 20
installed = False

while True:
	line = conn.recv(10000).decode("utf-8")
	# {'timestamp': '2020-10-09T11:18:06.861731+1000', 'flow_id': 2144724435, 'in_iface': 
	# 'h3-eth0', 'event_type': 'alert', 'src_ip': '10.0.0.4', 'src_port': 8081, 
	# 'dest_ip': '10.0.0.1', 'dest_port': 53757, 'proto': 'TCP', 
	# 'alert': {'action': 'allowed', 'gid': 1, 'signature_id': 0, 'rev': 0, 'signature': 'Ports Scanned', 'category': '', 'severity': 3}}
	try:
		split = line.split('\n')

		for i in split:
			if (i == ''):
				continue
			# print(i)
			parsed = json.loads(i)


			if (parsed['proto'] == 'TCP' and parsed['alert']['signature'] =='Ports Scanned'):
				pass
				# srcIP = parsed['src_ip']
			# 	print(parsed["timestamp"])
				# date = datetime.datetime.strptime(parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
				# if (not installed):
				# 	print("GETTING HERE!")
				# 	os.system("sudo ovs-ofctl del-flows s1")
				# 	os.system("sudo ovs-ofctl add-flow s1 dl_type=0x0800,nw_src=10.0.0.1,actions=drop")
				# 	os.system("sudo ovs-ofctl add-flow s1 dl_type=0x0800,nw_src=10.0.0.4,actions=drop")
				# 	installed = True

				# if (srcIP in blist):
				# 	diff = date - blist[srcIP]

				# 	if diff.total_seconds() >= hardTimeOut:
				# 		del blist[srcIP]
				# 	else:
				# 		continue

				# 	if srcIP not in wlist:

				# 		blist[srcIP] = date
				# 		for key in blist:
						
				# 		print('------------------------')
				# 		print('Current Flow Table for s1')
				# 		os.system("sudo ovs-ofctl dump-flows s1")
			# print(parsed)
			# sort out the logic
			
		# if parsed['tcp']['rst'] >= 200:  # If we've gotten more than 200 TCP RST packets
		# 	print("!!!!!!!!!!!!!!!!!!!!!!!!!!" + parsed)
		# 	srcIP = parsed['src_ip']
		# 	print(parsed["timestamp"])
		# 	date = datetime.datetime.strptime(parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
					
		# 
					
	except Exception as e:
		print("Error:", e)
		if ('data' in str(e)):
			print("------------------ ERROR ----------------------------")
			print(line)
		continue

sock.close()
