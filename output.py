import socket
import sys
import datetime
import os
import json
import threading


os.system("sudo ovs-ofctl del-flows s1")
os.system("rm eve.sock")
os.system("pkill -f suricata") # Remove all instances of suricata

'''
ONOS Mode works off an ONOS controller
CLI Mode (where ONOS = False) is more crude and just uses os library and ovs - ofctl to manages installation
'''
onosMode = False
anomalyMode = False


hardTimeOut = 10
internalIPs = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"}

if onosMode:
    ingressPort = {"of:0000000000000001": [1, 3], "of:0000000000000005": [2]};
    # For ONOS model
    postTo = "http://127.0.0.1:8181/onos/v1/flows/"
    auth = ('onos', 'rocks')
else:
    suricataInterfaces = {'h3-eth0':  's1', 'h8-eth0': 's5'} 
    ingressPort = {'s1': [1], 's5' : [2]};

def reflectedSpoofProtection():
    for switch in ingressPort:
        for port in ingressPort[switch]:
            for key in internalIPs:
                print(f"{switch} {port} {key}")
                cmd = "sudo ovs-ofctl add-flow " + switch + " hard_timeout=0,priority=65535,in_port="+str(port)+",dl_type=0x0800,nw_src="+str(key)+",actions=drop"
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
                            "ip": key + "/32"
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

    requests.post("http://127.0.0.1:8181/onos/v1/flows/",
                  data=json.dumps(pay_load_to_post), auth=('onos', 'rocks'))

def generateBlockingRuleONOS(ip, timeout=60, id="of:0000000000000001", isPermanent=False):
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
                            "ip": ip + "/32"
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

'''
Function for installing rule and differentiates between ONOS Mode and CLI Mode
Each thread has its own blist dictionary so shouldn't cause a race condition
'''
def installRule(switch, timeout, srcIP, date, blist) :
    if srcIP not in internalIPs:
        print("Installing on switch: " + switch)
        if (not onosMode):
            os.system("sudo ovs-ofctl del-flows " + switch)
            blist[srcIP] = date
            for key in blist:
                os.system("sudo ovs-ofctl add-flow "+switch+" hard_timeout=" + str(
                    hardTimeOut) + ",dl_type=0x0800,nw_src=" + str(key) + ",actions=drop")
            
            # reflectedSpoofProtection()
        else:
            blist[srcIP] = date
            for key in blist:
                print("Generate new flow rule addition")
                x = requests.post("http://127.0.0.1:8181/onos/v1/flows/",
                                    data=generateBlockingRuleONOS(key, timeout=10), auth=auth)
            

# TODO : Fix this 
if (onosMode):
    reflectedSpoofProtectionONOS()
else:
    reflectedSpoofProtection()


class SuricataConnection (threading.Thread):
    def __init__(self, threadID, name, sock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sock = sock

    def run(self):
        print ("Starting " + self.name)
        print("Reading from sock")
        blist = {}
        # For anomaly mode
        dests = {} #{ip : (, )} # {ip : (timestamp, msgsFromSuricata) packet count

        while True:
            line = self.sock.recv(475).decode("utf-8")
            try:
                lines = line.split('\n')
                for i in lines:
                    try:
                        if (i == ''):
                            continue
                        parsed = json.loads(i)
                        print(parsed)
                        if (str(parsed['proto']) == 'ICMP') or (parsed['proto'] == u'TCP' and int(str(parsed['alert']['signature_id'])) == 1):
                            if (not anomalyMode):
                                ''' 
                                Just in normal black list mode 
                                '''
                                srcIP = parsed['src_ip']
                                date = datetime.datetime.strptime(
                                    parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")

                                if (srcIP in blist):
                                    diff = date - blist[srcIP]
                                    if diff.total_seconds() >= hardTimeOut:
                                        del blist[srcIP]
                                    else:
                                        continue

                                switch = suricataInterfaces[parsed['in_iface']]

                                installRule(switch, hardTimeOut, srcIP, date, blist )
                                
                            else: 
                                '''
                                Basic anomaly mode
                                '''
                                median = 3
                                stdDev = 1

                                srcIP = parsed['src_ip']
                                date = datetime.datetime.strptime(
                                    parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")

                                if (srcIP in blist):
                                    diff = date - blist[srcIP]
                                    if diff.total_seconds() >= hardTimeOut:
                                        del blist[srcIP]
                                    else:
                                        continue


                                if srcIP not in dests:
                                    dests[srcIP] = [date, 1]
                                else :
                                    dests[srcIP][1] += 1
                                
                                print(dests)

                    except Exception as e:
                        print(e)
                        # print(i)
                        continue
            except Exception as e:
                print(e)
                # print(i)
                continue


server_address = "eve.sock"
sock = socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(5)

threads = []
for i in range(2):
    conn, addr = sock.accept()
    print("connection accepted...if you havent started suricata\nit means you have some \nsuricata processes still \nleft to kill do this with \n pkill -f suricata")

    thread = SuricataConnection(i, "Thread-"+str(i), conn)
    # Start new Threads 
    thread.start()
    # Add threads to thread list
    threads.append(thread)
for t in threads:
    t.join()

sock.close()


