Each file is self documentng

For full documentation please read the documentation folder.
You will need
suricata,
onos and
python3.7 to run all the files properly.

briefly all the files, 

h3suricmds -> sets up suricata with the CURRENT mirror.py on h3. So run this once you have run xterm h3 in mininet
h8suricmds -> sets up suricata with the CURRENT mirror.py on h8. So run this once you have run xterm h8 in mininet

output.py -> is our automated blocking program(abp), that installs rules on switches or sends rules to ONOS, depending on the mode
It also sets up the socket that suricata, sends rules based on the alerts that suricata sends it.
It currently is configured to connect to a max of 4 suricatas simulatenously however if you want to change that just updated suricatasNo field in the program
sudo python3.7 output.py [onos]

[onos] field runs the program such it connects to and sends rules to onos controller. Connects to the default onos rest ip, 
at http://127.0.0.1:8181/onos/v1/ .



mirror.py -> is the base topology that we ran all our experiments with.
sudo python mirror [onos]

[onos] field runs the topology such it connects connect to an onos controller

If you run mirror in onos mode, make sure you run output.py in onos mode


UsefulSynFloodScripts -> some useful scripts for testing syn floods

SuricataFilesMirror -> this folder contains a mirror of our suricata configuration and the rules that we used. Copy these into your own suricata installation, 
in the appropriate directories given at the top of each of those files

Launch simulatenous -> is the way simulatenous experiments were conducted where, run the first.sh  to acquire a file lock and run rest.sh, which will wait for the lock to be given up, in all other terminals.
Then press enter on the first.sh, which will release the file lock and all the terminals will run the commands after the flock cmds.

Documentation -> As much documentation as we had time to write.

