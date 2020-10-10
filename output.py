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

						blist[srcIP] = date
						for key in blist:
							os.system("sudo ovs-ofctl add-flow s1 hard_timeout=60,dl_type=0x0800,nw_src="+str(key)+",actions=drop")
						
						print('------------------------')
						print('Current Flow Table for s1')
						os.system("sudo ovs-ofctl dump-flows s1")
					

			except Exception as e:
				continue
			# try:

			# except:
			# 	print("HERE!")
 			# srcIP = str(parsed['src_ip'])
			# if srcIP not in blist:
			# 	os.system("sudo ovs-ofctl del-flows s1")
			# 	blist[srcIP] = True
				
			# 	print("Readding" + blist)
			# 	for key in blist:
			# 		os.system("sudo ovs-ofctl add-flow s1 priority=65535,hard_timeout=300,nw_src="+str(srcIP)+",actions=drop")

				
			
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
		print(e)
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
		
	
