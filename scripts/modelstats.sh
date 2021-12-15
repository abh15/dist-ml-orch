#!/bin/bash
for i in {10..59}
do
   docker logs mn.fc.$i | tail -3 | awk 'FNR == 1'
done