ovs-vsctl del-port s5-eth3
ovs-vsctl add-port s5 s5-eth3 -- --id=@p get port s5-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s5 mirrors=@m
suricata -c ../suricata-3.1/suricata.yaml -i h8-eth0