ovs-vsctl del-port s1-eth2
ovs-vsctl add-port s1 s1-eth2 -- --id=@p get port s1-eth2 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m
#ovs-vsctl del-port s5-eth2
#ovs-vsctl add-port s5 s5-eth2 -- --id=@p get port s5-eth2 -- --id=@m create mirror name=m1 select-all=true output-port=@p -- set bridge s5 mirrors=@m