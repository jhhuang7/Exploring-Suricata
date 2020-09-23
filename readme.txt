Here's the file with all the scripts that I've used so far, you'll also see in the vm config that there's two network cards.

EVERYTHING IS HARDCODED IN THIS EXAMPLE

DOS PROTECTION FROM h1 (attacker) to h5 (host)


What'll you need to do to get Suricata running is in this folder:
Vscode is also installed if you want to open this folder in vscdoe just do the cmd:

/snap/bin/code .


Suricata is installed at ~/suricata-3.1/ and it can be worth opening the suricata.yaml to see what i've done.
The rule files suricata will match on are found in the suricata.yaml and can be located in the  ~/suricata-3.1/rules/


THE RULSETS THAT ARE USED ARE FOUND IN THE RULES FOLDER RULES
 - Currently its matching 10 pkts in 60 seconds from 10.0.0.1 before alerting




STEPS FOR SURICATA
1. gnome-terminal . (opens a new terminal in this folder)

2. sudo python mirror.py (if you get a cannot move interface error just restart)
Opens a mininet topology tree topology and sets up port mirroring on a particular interface from s1 to h3

3. in mininet run xterm h3

4. in the xterm run sudo ./cmds.sh  (run suricata)

5. in another gnome-terminal run sudo python output.py

6. In mininet open up h1 in xterm  
    hping3 10.0.0.5 -1 --fast (Starts the dos attack)
    It should have an rtt of 0 after it sends 3 packets.
    or stop printing completely

