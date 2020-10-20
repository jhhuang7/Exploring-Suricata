ovs-vsctl del-port s1-eth2
ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m
suricata -c ../suricata-3.1/suricata.yaml -i h3-eth0