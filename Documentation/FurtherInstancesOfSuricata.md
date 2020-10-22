As our system is currently quite low level, setting an extra instance of Suricata in this system requires a little bit of effort.



1. Add at least 2 extra hosts connected to a switch in mirror.py (some examples are commented out)
2. After this run `links`, in mininet  find out what interface the host you intend run to suricata on is connected to the switch you want to monitor traffic through

    * For example you'll see that the h3 host is connected thorugh a s1-eth2 <->  h3-eth0 link.

3. Before you run output.py, update the following fields in the program. The current version requires makes use of some hardcoded values. so you'll have to update them, based on what you're planning to do. So in output make the following changes, around line ~50.

##### For sys call (not onos) mode: 
```python
    ingressPort = {'s1': [1], 's5' : [2]};
    suricataInterfaces = {'h3-eth0':  's1', 'h8-eth0': 's5'} 
    ingressPort = {'s1': [1], 's5' : [2], 'newSwitch', [outWardFacingInterfaces]}; # For reflected spoof protection (optional)

    #Add interface on host and switch being monitored
    suricataInterfaces = {'h3-eth0':  's1', 'h8-eth0': 's5', <'interfaceOnHost'> : <'switchBeingMonitored'> } 
```

##### For onos mode
```python

    ingressPort = {"of:0000000000000001": [1], "of:0000000000000005": [2], 'newSwitch', [outWardFacingInterfaces] };  #For reflected spoof protection (optional)

    #Add interface on host and switch being monitored
    suricataInterfaces = {'h3-eth0':  "of:0000000000000001", 'h8-eth0': "of:0000000000000005", <'interfaceOnHost'> : <'switchBeingMonitoredONOSDeviceID'>} 

```


After all this make sure output.py is running in, to launch output.py
    * Sys calls mode, run `sudo python3.7 output.py`
    * ONOS mode, run `sudo python3.7 output.py onos`


4. `xterm [host you want to run suricata on]`

5. Run use the launchSuricata.py to set up port mirroring and run suricata. 

    * Going back to the h3 example the command that you would use would be :  `sudo python3.7 launchSuricata s1-eth2 h3-eth0` where s1-eth2, is the interface on the switch you intend to monitor traffic through and h3
 