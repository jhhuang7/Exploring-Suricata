Original Tutorial Used Found:  csie.nqu.edu.tw/smallko/sdn/ids_ips_suricata.htm


### This tutorial takes you through running a basic suricata attack and defense with your system

### Preqs

Before you start these steps, please ensure, that you have changed your Suricata files to exactly match the ones in the SuricataFilesMirror. 
Next please ensure that you have python3.7 installed, We have made use of fstrings liberally.

SuricataFilesMirror/emerging-rules.icmp contains files for the rules for when the python program will get alerted, and install a rule. At the moment it will send python an alert if it detects 10 icmp packets with 10 seconds. Change these thresholds in suricata3-1/rules/emerging-rules however you see fit.


0. Launch your onos controller. (If you want to run in ONOS mode)
1. Launch mirror.py, 
    * Flows installed sys calls, run `sudo python mirror.py`
    * Flows installed through ONOS, run `sudo python mirror.py onos`

This should launch mininet.

2. In a separate terminal, launch output.py
    * Sys calls mode, run `sudo python3.7 output.py`
    * ONOS mode, run `sudo python3.7 output.py onos`

output.py clears any extraneous suricata processes, clears flows of off the s1 and s5 switches so that a fresh experiment can be run.


3. In mininet run `xterm h1` and `xterm h3`. h1 will be our attacker and h3 is where suricata will reside.

4. in the `xterm h3` terminal run `./h3suricmds.sh`. This set up the portmirroring and connect to the python socket that output.py has setup. The python program should display some message stating. "Connection Accepted."

5. Launch an attack from h1 to any of h2, h4, h5, h6, using hping3.
Example command, hping -1 --fast 10.0.0.4 , will launch a ICMP flood pretty slowly to h4, however this should trigger the rules given in the emerging-icmp.rulesets, stop the attack and install a flow rule. You should be able to see the attack stop in the hping3, ping return messages. 



If you want to restart output.py, make sure you Ctrl+C suricata, ensure that you run the output.py first.


-> Modify the thresholds suricata-3.1/rules/emerging-icmp.rules and have a play around!

### Multiple Instances of Suricata

Connecting up another instance of suricata for testing has already been set and ready to go. It is figured to reside on h8 with it being to the s5 switch. As stated in our report output.py has already been set up with multithreading, so all you need to do is ensure that suricataNo variable is higher than the number of suriata instances you're planning to do. Currently it is configured at 4 instances of Suricata / threads.

Thus launch, `xterm h8` , and run `./h8suricmds.sh` and when you launch attacks through switch s5, you'll see it that if s5, launches too many packets, it will get blocked.


For setting up further instances of suricata please refer to the FurtherInstancesOfSuricata.md for the relevant documentation.


