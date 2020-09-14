Here's the file with all the scripts that I've used so far, you'll also see in the vm config that there's two network cards.



What'll you need to do to get Suricata running is in this folder:
Vscode is also installed if you want to open this folder in vscdoe just do the cmd:

/snap/bin/code .


Suricata is installed at ~/suricata-3.1/ and it can be worth opening the suricata.yaml to see what i've done.
The rule files suricata will match on are found in the suricata.yaml and can be located in the  ~/suricata-3.1/rules/
At the moment its set up to basically  just matching/alert on ICMP (ping ) messages

STEPS FOR SURICATA
1. gnome-terminal . (opens a new terminal in this folder)

2. sudo python mirror.py (if you get a cannot move interface error just restart)
Opens a mininet topology h1<->s1<->h2, with h3 being the host that suricata will 
sit on and all the trafic through the switch gets mirrored to it.

3. in mininet run xterm h3

4. in the xterm run sudo ./cmds.sh  (this will set up the port mirroring and run suricata)


5. from another terminal in portmirroring run sudo python3.7 output.py

In suricata(xterm terminal) you should something like reconnected socket , i've got suricata set up atm to talk to output.py through 
that eve.sock file/socket.

7. In mininet run h1 ping -c 10 h2 you should see some messages printing in the output.py terminal

At the moment it calculates the difference between two packets and if the duration is less than a second it installs a 
rule onto s1 to drop all packets from 10.0.0.1 s1.
