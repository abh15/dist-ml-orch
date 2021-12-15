# dist-ml-orch

Implementation of distributed orchestration for federated learning. This work was done as part of master's thesis *Distributed machine learning function orchestration in 5G networks*.

This implementation has 3 components:

[Containernet v3.1](https://github.com/containernet/containernet) is used to create a topology with Federated clients and servers as end hosts

[Distributed MLFO](https://github.com/abh15/mlfo-dist) is extension of Machine learning function orchestrator based on framework specified in  ITU-T Y.3172 

[abh15/flower](https://github.com/abh15/flower) allows to start federated clients and servers with specified configuration via a REST interface



## Prerequisites
Ubuntu 20.04

128 core CPU

Clone [Containernet v3.1](https://github.com/containernet/containernet) and install using Option 1 Bare-metal installation

Install [ONOS v2.7.0](https://wiki.onosproject.org/display/ONOS/Developer+Quick+Start) 


## Start ONOS

Terminal 1

`cd onos`

`bazel run onos-local -- clean debug`

Terminal 2

`cd onos`

`tools/test/bin/onos localhost`

onos> `app activate org.onosproject.openflow`

onos> `app activate org.onosproject.fwd`



## Usage
### Create topology
1. Copy scripts directory to containernet directory

2. Make sure promconfig is set to correct path

3. `cd containernet/scripts`
	
	In terminal 1 excute the following and wait till the topology is created 

	`sudo python3 topo.py <num of cohorts>  #e.g sudo python3 topo.py 5`

	In terminal 2 execute following to update cpu limits and start background traffic application

	`bash init.sh <num of cohorts> #e.g bash init.sh 5`

	In terminal 3 execute following to test ping reachibility of topology nodes
	
	`bash pingtest.sh`


### Send intent
We send intents to MLFO from a remote machine. 

*mlfoadd* gives address:mlfo exposed port of remote machine where the mlfo is running

*cohortdistr* specifies how 50 clients are divided into cohorts (e.g 30,10,10 or 10,10,10,10,10). Number of cohorts should be same as that created in topology.

*intentdist* specifies which intent yaml to send for which cohort. Currently we only have 3 intents which work

*sameserverdist* specifies if multiple cohorts should use same FL server. Currently this is **ignored**

*avgalgodist* specifies which aggregation algorithm to use. Currently only FedAvg is supported

*fracfit* fraction of clients to use for fitting

*minfit* Minimum num of clients to fit

*minav* Minimum number of clients required to start FL rounds

*numround* Number of FL rounds

`cd intents`

Execute the following to send intents to MLFO and to start the FL process

`python3 sendintent.py`

### Monitoring 
1. Add Grafana.

	`docker run -d -p 3000:3000 grafana/grafana`

2. Navigate to  http://10.66.2.142:3000. Go to configuration > add data source > add prometheus. Add the following HTTP URL and click save and test.

	`http://10.66.2.142:9090`

3. Add the dashboard by importing *monitoring/dashboard.json* file.


5. Open daszweite dashboard at:
	`http://10.66.2.142:3000/d/ouQy_xDnk/daszweite`



### Send meter
This script sets meter for FL clients uplink at 100Mbps and downlink at 100Mbps.  IN_PORT number in line 25 needs to be set to correct cohort number which needs to be metered(e.g 1, 2, 3)

`sudo python3 sendmeter.py` 


## Misc commands

### Reset mininet
`sudo mn -c`

### Port mapping
Flower: 

		5000 —> REST

	    6000 —> FLWRINTERNAL

MLFO: 

		8000 —> REST

	  	9000 —> MLFO SERVER

### Send test intent
`curl -v -F file=@intent.yaml 'http://localhost:8000/receive'`

### Open bash shell at one of the nodes

sudo docker exec -it mn.fed.1 /bin/bash

sudo docker exec -it mn.fc.11 /bin/bash

sudo docker exec -it mn.mo.1 /bin/bash
