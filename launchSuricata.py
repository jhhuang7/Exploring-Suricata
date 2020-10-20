import os
import sys

# Sets up port mirroring 
# Launches Suricata
# Example in cmds.sh
# for the s1 suricata (cmds.sh): sudo python launchSuricata s1-eth2 h3-eth0
# for the s4 suricata (cmds.sh): sudo python launchSuricata s5-eth3 h8-eth0

if len(sys.argv) != 3:
    print("sudo python launchSuricata interfaceOnSwitch interfaceOnHost")
else:
    print(f"Make sure the  entry {sys.argv[2]} : {sys.argv[1][0:2]} is in the suricataInterfaces dictionary")
    os.system('ovs-vsctl del-port ' + sys.argv[1])
    os.system(f"ovs-vsctl add-port {sys.argv[1][0:2]} {sys.argv[1]} -- --id=@p get port {sys.argv[1]} -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge {sys.argv[1][0:2]} mirrors=@m")
    os.system(f"suricata -c ../suricata-3.1/suricata.yaml -i {sys.argv[2]}")
