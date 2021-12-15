import sys
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel('info')

promconfig="prometheus.yml"

net = Containernet(controller=Controller, switch=OVSSwitch)
info('*** Adding controller\n')

net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6653, protocols="OpenFlow13")
info('*** Adding docker containers\n')

numcohorts = int(sys.argv[1])
aggsw = net.addSwitch("aggsw10",cls=OVSSwitch,protocols="OpenFlow13")
satsw = net.addSwitch("satsw11",cls=OVSSwitch,protocols="OpenFlow13")
prom = net.addDocker('prom.0', volumes=[promconfig+":/etc/prometheus/prometheus.yml"], ip='10.0.0.100', dimage="prom/prometheus-linux-amd64:main",ports=[9090], port_bindings={9090:9090}, publish_all_ports=True)
prom.start()
cloud0 = net.addDocker('cloud.0', ip='10.0.0.1', dimage="abh15/mlfo:latest")#,ports=[8000], port_bindings={8000:8999}, publish_all_ports=True)
cloud0.start()
bgtserver = net.addDocker('appserv.0', ip='10.0.0.2', dimage="abh15/mlfo:latest")
bgtserver.start()

# Add federated servers
for cohort in range (1, numcohorts+1):
    fedserver = net.addDocker("fed."+ str(cohort), ip='10.0.0.'+str(100+cohort), dimage="abh15/flwr:latest")
    fedserver.start()
    net.addLink(fedserver, aggsw, bw=500)

net.addLink(cloud0, aggsw, bw=500)
net.addLink(prom, aggsw, bw=500)
net.addLink(bgtserver, aggsw, bw=500)
net.addLink(satsw, aggsw, cls=TCLink, delay="12ms", bw=500)

#===========================================================================

intentport = 8000+1
edgesw = net.addSwitch("swEdge12",cls=OVSSwitch,protocols="OpenFlow13")
mlfonode = net.addDocker("mo.1", ip="10.0.1.1", dimage="abh15/mlfo:latest", ports=[8000], port_bindings={8000:intentport}, publish_all_ports=True)
mlfonode.start()
bgtapp1 = net.addDocker("app.1", ip="10.0.1.2", dimage="abh15/mlfo:latest")
bgtapp1.start()


net.addLink(mlfonode, edgesw, bw=500)
net.addLink(bgtapp1, edgesw, bw=500)

for sw in range(1, 6):
    campsw = net.addSwitch("swCampus"+str(sw),cls=OVSSwitch,protocols="OpenFlow13")
    for fcli in range(0,10):
        fclient = net.addDocker("fc."+ str(sw)+ str(fcli), ip="10.0.1." + str(sw)+ str(fcli), dimage="abh15/flwr:latest")
        fclient.start()
        net.addLink(fclient, campsw, bw=500)
    net.addLink(campsw, edgesw, bw=500)

net.addLink(edgesw, satsw, cls=TCLink, delay="12ms", bw=500)


info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
