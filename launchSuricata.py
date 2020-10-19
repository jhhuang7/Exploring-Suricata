import os
import sys

if len(sys.argv) != 3:
    print("sudo python launchSuricata interfaceOnSwitch interfaceOnHost")

os.system('ovs-vsctl del-port s1-eth2')
os.system("ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m")
os.system("suricata -c ../suricata-3.1/suricata.yaml -i h8-eth0"
