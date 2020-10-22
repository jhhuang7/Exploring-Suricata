import socket
import sys
import datetime
import os
import json
import threading
import requests


#####--- START OF CONFIGURATION OPTIONS-----####

# CONFIGURATION OPTIONS / GLOBAL VARIABLES
'''
ONOS Mode works off an ONOS controller
CLI Mode (where ONOS = False) is more crude and just uses os library and ovs - ofctl to manages installation
'''

if (len(sys.argv) == 2 and sys.argv[1] == "onos"):
    onosMode = True
else:
    onosMode = False
'''
False : runs in blacklist which works solely of the suricata
True : runs in basic anomaly mode with hardcoded means medians
'''
anomalyMode = False

'''
How long block rules are on the switch for
'''
hardTimeOut = 10

'''
Print Parsed
'''
printParsed = False

# HARDCODED VALUES
'''
Hardcoded internals ips of our network, Future work is detect this using the onos controller
'''
internalIPs = {"10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"}


'''
Hardcoded : the switches that suricata will be connected to
'''
if onosMode:
    '''
    Hardcoded : switches and the ports that lead outside of our system
    '''
    ingressPort = {"of:0000000000000001": [1], "of:0000000000000005": [2]};
    # For ONOS model
    postTo = "http://127.0.0.1:8181/onos/v1/flows/"
    auth = ('onos', 'rocks')
    '''
    Hardcoded : the switches that suricata will be connected to
    '''
    suricataInterfaces = {'h3-eth0':  "of:0000000000000001", 'h8-eth0': "of:0000000000000005"} 

else:
    '''
    Hardcoded : switches and the ports that lead outside of our system
    '''
    ingressPort = {'s1': [1], 's5' : [2]};

    '''
    Hardcoded : the switches that suricata will be connected to
    '''
    suricataInterfaces = {'h3-eth0':  's1', 'h8-eth0': 's5'} 

#####--- END OF CONFIGURATION OPTIONS-----####

'''
Used in not onos mode, where it iterates through all internal ips currently not used for perfomance reasons.
'''
def reflectedSpoofProtection():
    for switch in ingressPort:
        for port in ingressPort[switch]:
            for key in internalIPs:
                print(f"{switch} {port} {key}")
                cmd = "sudo ovs-ofctl add-flow " + switch + " hard_timeout=0,priority=65535,in_port="+str(port)+",dl_type=0x0800,nw_src="+str(key)+",actions=drop"
                os.system(cmd)


'''
Used in not onos mode, where it iterates through all internal ips and 
'''
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
                    "deviceId": switch,
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
                            "port": str(port)
                        },
                        ]
                        }
                    })

    print(pay_load_to_post)
    requests.post("http://127.0.0.1:8181/onos/v1/flows/",
                  data=json.dumps(pay_load_to_post), auth=('onos', 'rocks'))

'''
Populates the required fields for an ONOS blocking rule
'''
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
            x = requests.post("http://127.0.0.1:8181/onos/v1/flows/", data=generateBlockingRuleONOS(srcIP, timeout=hardTimeOut, id=switch), auth=auth)
            


'''
Thread instance which manages an instance of SURICATA
'''
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


        # For BASIC anomaly mode
        dests = {} #{ip : (, )} # {ip : (timestamp, msgsFromSuricata) packet count

        while True:
            line = self.sock.recv(475).decode("utf-8") # Reads from socket
            try:
                lines = line.split('\n')
                for i in lines:
                    try:
                        if (i == ''):
                            continue
                        parsed = json.loads(i)
                        
                        # If protocol in the packet is ICMP or Matches one our signatures
                        if (str(parsed['proto']) == 'ICMP') \
                                or (parsed['proto'] == u'TCP' and int(str(parsed['alert']['signature_id'])) == 1):
                            
                            if (printParsed) :
                                print(parsed)

                            if (not anomalyMode):
                                ''' 
                                Just in normal black list mode 
                                '''
                                srcIP = parsed['src_ip']
                                date = datetime.datetime.strptime(
                                    parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
                                

                                '''
                                As installing rule is expensive, if the program has already installed a
                                rule on that switch within the last hardOutTimeout seconds
                                don't install a rule, else proceed.
                                '''
                                if (srcIP in blist):
                                    diff = date - blist[srcIP]
                                    if diff.total_seconds() >= hardTimeOut:
                                        del blist[srcIP]
                                    else:
                                        continue

                                # Gets the switch that Suricata is connected to 
                                # and installs the rules to that switch
                                switch = suricataInterfaces[parsed['in_iface']]

                                # Installs the rule
                                installRule(switch, hardTimeOut, srcIP, date, blist)
                                
                            else: 
                                '''
                                Basic anomaly mode
                                '''
                                median = 5
                                minMed = 3
                                maxMed = 10


                                stdDev = 1
                                threshold = 2; # make sure this is the same as rules

                                srcIP = parsed['src_ip']
                                date = datetime.datetime.strptime(
                                    parsed["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
                                    
                                if (srcIP in blist):
                                    diff = date - blist[srcIP]
                                    if diff.total_seconds() >= hardTimeOut:
                                        del blist[srcIP]
                                    else:
                                        continue


                                if srcIP not in dests and srcIP not in internalIPs:
                                    print("new source ip is in dests adding one")
                                    dests[srcIP] = [date, 1]

                                else :
                                    print("Source ip is in dests adding one")
                                    cDate = dests[srcIP][0]

                                    diff = date - cDate;
                                    if (diff.total_seconds() <= threshold) :
                                        dests[srcIP][1] += 1    

                                        if (dests[srcIP][1] >= median + 3 * stdDev) :
                                            print(f"Over 3 devs in the last {threshold}")
                                            if (srcIP in blist):
                                                diff = date - blist[srcIP]
                                                if diff.total_seconds() >= hardTimeOut:
                                                    del blist[srcIP]
                                                else:
                                                    continue

                                            switch = suricataInterfaces[parsed['in_iface']]

                                            installRule(switch, hardTimeOut, srcIP, date, blist )
                                    else:
                                        print("Restarting the threshold")
                                        print(f"Time since last period.... {(date - cDate).total_seconds() - threshold}")
                                        dests[srcIP][0] = date

                                        # Move mean
                                        
                                        
                                        print(f"Time periods of zero {timePeriodsOfZero}")
                                        
                                        dests[srcIP][1] = 1

                    except Exception as e:
                        # print(e)
                        # print(i)
                        continue
            except Exception as e:
                # print(e)
                # print(i)
                continue




if __name__ == '__main__':
    '''
    Cleaning up processes before starting a new instance
    '''
    os.system("sudo ovs-ofctl del-flows s1")
    os.system("sudo ovs-ofctl del-flows s5")
    os.system("rm eve.sock")
    os.system("pkill -f suricata") # Remove all instances of suricata

    '''
    Install reflected spoof protection
    '''
    if (onosMode):
        reflectedSpoofProtectionONOS()
    else:
        pass
        # reflectedSpoofProtection()



    # Sets up unix file socket in eve.sock which is what suricata expects to connect to in the suricata.yaml file
    # Sockets gives this program json which is parsed
    server_address = "eve.sock"
    sock = socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    sock.listen(5)

    threads = []
    #Amount of suricatas before the main thread stops accepting new connectionSS
    suricatasNo = 4
        
    for i in range(suricatasNo):    
        conn, addr = sock.accept()
        print("Connection Accepted. \nNOTE:If you havent started suricata\nit means you have some \nsuricata processes still \nleft to kill do this with \n pkill -f suricata")
        
        # Mangaes the suricata connected to the conn socket in this thread
        thread = SuricataConnection(i, "Thread-"+str(i), conn)
        # Start new Threads 
        thread.start()
        # Add threads to thread list
        threads.append(thread)

    for t in threads:
        t.join()

    sock.close()
