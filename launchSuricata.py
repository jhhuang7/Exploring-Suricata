import os
import sys

# Sets up port mirroring 
# Launches Suricata
if len(sys.argv) != 3:
    print("sudo python launchSuricata interfaceOnSwitch interfaceOnHost")
else:
    print(sys.argv)
    os.system('ovs-vsctl del-port ' + sys.argv[1])
    os.system(f"ovs-vsctl add-port {sys.argv[1][0:2]} {sys.argv[1]} -- --id=@p get port {sys.argv[1]} -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge {sys.argv[1][0:2]} mirrors=@m")
    os.system(f"suricata -c ../suricata-3.1/suricata.yaml -i {sys.argv[2]}")
