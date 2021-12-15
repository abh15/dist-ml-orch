#!/usr/bin/python3
import requests

#For campus switches effective is 18750 *3

headers={'Content-Type':'application/json', 'Accepts': 'application/json'}

# data1 creates meter bands, data2 assigns meter band to particular flow (flow for target cohort)
# This block sets meter for data sent from FL Cli to FL server
for i in range(1,4):
    url1= 'http://10.66.2.142:8181/onos/v1/meters/of%3A000000000000000'+str(i)
    data1= '{ "deviceId": "of:000000000000000'+str(i)+'", "unit": "KB_PER_SEC", "burst": true, "bands": [ { "type": "DROP", "rate": "33000", "burstSize": "33000" } ] }'
    response = requests.post( url1, data=data1, headers=headers, auth=('onos', 'rocks') )
    for j in range(1,11):
        url2= 'http://10.66.2.142:8181/onos/v1/flows/of%3A000000000000000'+str(i)+'?appId=org.onosproject.core'
        data2= '{ "priority": 10000, "timeout": 0, "isPermanent": true, "deviceId": "of:000000000000000'+str(i)+'", "treatment": { "instructions": [ { "type": "OUTPUT", "port": "11" }, { "type": "METER", "meterId": 1 } ] }, "selector": { "criteria": [ { "type": "IN_PORT", "port": "'+str(j)+'" } ] } }'
        response = requests.post( url2, data=data2, headers=headers, auth=('onos', 'rocks') )
        
# Value of port in "type": "IN_PORT" in data2 line needs to be set to correct cohort(one with 30 clients) (valid values are 1, 2, 3)
# This block sets meter for data sent from FL server to FL cli
url1= 'http://10.66.2.142:8181/onos/v1/meters/of%3A000000000000000a'
data1= '{ "deviceId": "of:000000000000000a", "unit": "KB_PER_SEC", "burst": true, "bands": [ { "type": "DROP", "rate": "100000", "burstSize": "100000" } ] }'
response = requests.post( url1, data=data1, headers=headers, auth=('onos', 'rocks') )
url2= 'http://10.66.2.142:8181/onos/v1/flows/of%3A000000000000000a?appId=org.onosproject.core'
data2= '{ "priority": 10000, "timeout": 0, "isPermanent": true, "deviceId": "of:000000000000000a", "treatment": { "instructions": [ { "type": "OUTPUT", "port": "7" }, { "type": "METER", "meterId": 1} ] }, "selector": { "criteria": [ { "type": "IN_PORT", "port": "1" }, { "type": "ETH_TYPE", "ethType": "0x800" }, { "type":"IPV4_DST", "ip":"10.0.1.0/24" } ] } }'
response = requests.post( url2, data=data2, headers=headers, auth=('onos', 'rocks') )
