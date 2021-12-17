#!/bin/bash
for ((i=1;i<=$1;i++))
do
   docker update --cpus 2 mn.fed.$i
done
for i in {10..59}
do
   docker update --cpus 2 mn.fc.$i
done
docker exec -it -d mn.appserv.0 iperf -s
docker exec -it -d mn.app.1 iperf -c 10.0.0.2 -b 20m -t 2000s