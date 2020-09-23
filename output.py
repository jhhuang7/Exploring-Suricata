import socket
import sys
import datetime
import os
import json



os.system("rm eve.sock")

server_address = "eve.sock"
sock =  socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address);
sock.listen(1)

conn,addr =  sock.accept()

lastA = None
dosProtection = False
while True:
	line = conn.recv(10000).decode("utf-8")
	try:
		parsed = json.loads(line)

		if (parsed['proto'] == u'ICMP' and dosProtection == False) :
 			os.system("sudo ovs-ofctl del-flows s1")
			os.system("sudo ovs-ofctl add-flow s1 priority=65535,hard_timeout=300,nw_src=10.0.0.1,actions=drop")
			os.system("sudo ovs-ofctl add-flow s1 priority=65535,hard_timeout=300,nw_src=10.0.0.5,actions=drop")
			dosProtection = True

			
		# if (parsed['proto'] == u'ICMP' and parsed["src_ip"]=="10.0.0.1"):
		# 	if line == "proto":
		# 		continue
		# 	else:
		# 		a = datetime.datetime.strptime(parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
		# 		if lastA == None:
		# 			lastA = a
		# 			continue
		# 		else:
		# 			diff =  a - lastA
		# 			print("Difference is")
		# 			print(diff.total_seconds())
		# 			lastA = a

		# 			if (diff.total_seconds() < 1):
		# 				if not dosProtection:						
		# 					print("Adding flow")

		# 					os.system("sudo ovs-ofctl add-flow s1 priority=65535,hard_timeout=120,nw_src=10.0.0.2,actions=drop")


	except Exception as e:
		#print(e)
		#UNCOMMENT TO PRINT ERRORS
		continue

sock.close()

# # a = sock.recv(100)
# # print(a)


# while True:
# 	where = file1.tell()
# 	line = file1.readline()

# 	if not line:
# 		file1.seek(where)
		
# 	else:
# 		try:
# 			parsed = json.loads(line)


# 		except:
# 			continue	
		
	
