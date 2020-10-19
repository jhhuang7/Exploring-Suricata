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

conn,addr =  sock.accept()
onosMode = False
anomalyMode = False


median = 3
stdDev = 1

hardTimeOut = 10
blist = {}
internalIPs = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5","10.0.0.6"}

if onosMode:
	ingressPort = {"of:0000000000000001" : [1, 3]};
else:
	ingressPort = {'s1' : [1, 3]};
	#For ONOS model
	postTo = "http://127.0.0.1:8181/onos/v1/flows/"
	auth = ('onos','rocks')



def reflectedSpoofProtection():
	for switch in ingressPort:
		for port in ingressPort[switch]:
			for key in internalIPs:
				cmd = "sudo ovs-ofctl add-flow " + switch + \
						" hard_timeout=0,priority=65535,in_port="+str(port)+\
						",dl_type=0x0800,nw_src="+str(key)+",actions=drop"
				os.system(cmd)


def reflectedSpoofProtectionONOS():
	pay_load_to_post = {
	"flows": [
			
	]
	}
	print("Installing Reflection DOS Protection")

	for switch in ingressPort:
		for port in ingressPort[switch]:
			for key in internalIPs:
				pay_load_to_post["flows"].append({
					"priority": 41000,
					"timeout": 0,
					"isPermanent": True,
					"deviceId": "of:0000000000000001",
					"treatment": {

					}, "selector": {
						"criteria": [
						{
							"type": "IPV4_SRC",
							"ip": key+"/32"
						},
						{
							"type": "ETH_TYPE",
							"ethType": "0x0800"
						},
						{
							"type": "IN_PORT",
							"port": str(p)
						},
						]
						}
					})

	requests.post("http://127.0.0.1:8181/onos/v1/flows/", data = json.dumps(pay_load_to_post) , auth=('onos','rocks'))


def generateBlockingRuleONOS(ip, timeout=60,id="of:0000000000000001", isPermanent=False):
	return json.dumps({
		"flows": [{
				"priority": 42000,
				"timeout": timeout,
				"isPermanent": isPermanent,
				"deviceId": id,
				"treatment": {

				}, "selector": {
					"criteria": [
						{
							"type": "IPV4_SRC",
							"ip": ip+"/32"
						},
						{
							"type": "ETH_TYPE",
							"ethType": "0x0800"
						},

					]
				}
			}
		]
})

if (onosMode):
	reflectedSpoofProtectionONOS()
else:
	reflectedSpoofProtection()

while True:
	line = conn.recv(512).decode("utf-8")
	try:
		lines =  line.split('\n')
		for i in lines:
			try:
				if (i == '') :
					continue
				parsed = json.loads(i)

				if (str(parsed['proto']) == 'ICMP') or (parsed['proto'] == u'TCP' and int(str(parsed['alert']['signature_id'])) ==1):
					if (not anomalyMode) :
						srcIP = parsed['src_ip']
						date = datetime.datetime.strptime(parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
						if (srcIP in blist) :
							diff = date - blist[srcIP]
							if diff.total_seconds() >= hardTimeOut:
								del blist[srcIP]
							else:
								continue

						if srcIP not in internalIPs :

							if (not onosMode) :
								os.system("sudo ovs-ofctl del-flows s1")
								blist[srcIP] = date
								for key in blist:
									os.system("sudo ovs-ofctl add-flow s1 hard_timeout="+str(hardTimeOut)+",dl_type=0x0800,nw_src="+str(key)+",actions=drop")
							else:
								blist[srcIP] = date
								for key in blist:
									print("Generate new flow rule addition")
									x = requests.post("http://127.0.0.1:8181/onos/v1/flows/", data=generateBlockingRule(key, timeout=10), auth=auth)


			except Exception as e:
				print(e)
				print(i)
				continue
	except Exception as e:
		print(e)
		print(i)
		continue

sock.close()


