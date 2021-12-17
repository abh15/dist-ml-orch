#!/bin/bash
for ((i=1;i<=$1;i++))
do
        docker exec -it mn.cloud.0 ping -c 2 10.0.0.10$1
done
for i in {10..59}
do
        docker exec -it mn.fc.$i ping -c 2 10.0.0.1
done
