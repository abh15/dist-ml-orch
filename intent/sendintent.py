#!/usr/bin/python3
import requests
import sys
import time

"""" 
Script to send intent to MLFO running on a remote server
"""
mlfoadd = 'http://10.66.2.142:8001/receive'

#timegap in seconds is period in between two intents 
# timegap=1

# cohortdistr = [10,10,10,10,10]
# intentdist=['intent.yaml', '2intent.yaml', 'intent.yaml', '2intent.yaml', 'intent.yaml']
# #intentdist=['3intent.yaml', '3intent.yaml', '3intent.yaml', '3intent.yaml', '3intent.yaml']
# sameserverdist= ['nor','no','no','no','no']
# avgalgodist=['FedAvg','FedAvg','FedAvg','FedAvg','FedAvg']
# fracfitdist= ['0.5','0.5','0.5','0.5','0.5']
# minfitdist=['1','1','1','1','1']
# minavdist= ['1','1','1','1','1']
# numrounddist =['20','20','20','20','20']

# cohortdistr = [4,4,4,4,4,4,4,4,4,4,4,4]
# intentdist=['intent.yaml','2intent.yaml','intent.yaml', '2intent.yaml', 'intent.yaml', '2intent.yaml', 'intent.yaml', '2intent.yaml','intent.yaml', '2intent.yaml','intent.yaml', '2intent.yaml']
# #intentdist=['3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml']
# sameserverdist= ['nor','no','no','no','no','no','no','no','no','no','no','no']
# avgalgodist=['FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg']
# fracfitdist= ['0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5']
# minfitdist=['1','1','1','1','1','1','1','1','1','1','1','1']
# minavdist= ['1','1','1','1','1','1','1','1','1','1','1','1']
# numrounddist =['20','20','20','20','20','20','20','20','20','20','20','20']


# cohortdistr = [6,6,6,6,6,6,6,6]
# intentdist=['intent.yaml','2intent.yaml','intent.yaml', '2intent.yaml', 'intent.yaml', '2intent.yaml', 'intent.yaml', '2intent.yaml']
# #intentdist=['3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml','3intent.yaml']
# sameserverdist= ['nor','no','no','no','no','no','no','no']
# avgalgodist=['FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg','FedAvg']
# fracfitdist= ['0.5','0.5','0.5','0.5','0.5','0.5','0.5','0.5']
# minfitdist=['1','1','1','1','1','1','1','1']
# minavdist= ['1','1','1','1','1','1','1','1']
# numrounddist =['20','20','20','20','20','20','20','20']



# cohortdistr = [50]
# intentdist=['3intent.yaml']
# sameserverdist= ['nor']
# avgalgodist=['FedAvg']
# fracfitdist= ['0.5']
# minfitdist=['1']
# minavdist= ['1']
# numrounddist =['20']


cohortdistr = [30,10,10]
intentdist=['3intent.yaml', 'intent.yaml', '2intent.yaml']
sameserverdist= ['nor','no','no']
avgalgodist=['FedAvg','FedAvg','FedAvg']
fracfitdist= ['0.5','0.5','0.5']
minfitdist=['1','1','1']
minavdist= ['1','1','1']
numrounddist =['20','20','20']


# cohortdistr = [10,10,10]
# intentdist=['3intent.yaml', '3intent.yaml', '3intent.yaml']
# sameserverdist= ['nor','no','no']
# avgalgodist=['FedAvg','FedAvg','FedAvg']
# fracfitdist= ['0.5','0.5','0.5']
# minfitdist=['1','1','1']
# minavdist= ['1','1','1']
# numrounddist =['20','20','20']


# cohortdistr = [30]
# intentdist=['3intent.yaml']
# sameserverdist= ['nor']
# avgalgodist=['FedAvg']
# fracfitdist= ['0.5']
# minfitdist=['1']
# minavdist= ['1']
# numrounddist =['20']


def send(intentfile, ipstart, cohortsize, sameserver, avgalgo, fracfit, minfit, minav, numround):
    files = {'file': open(intentfile, 'rb')}
    payload = {'ipstart': ipstart, 'cohortsize' : cohortsize, 'sameserver': sameserver, 'avgalgo': avgalgo,
                'fracfit':fracfit, 'minfit':minfit, 'minav':minav, 'numround':numround}
    r = requests.post(mlfoadd, files=files, data=payload)
       
def main():
    octtraker = 10
    for i in range(len(cohortdistr)):
        cohort= cohortdistr[i]
        intent= intentdist[i]
        sameserver= sameserverdist[i]
        avgalgo=avgalgodist[i]
        fracfit= fracfitdist[i]
        minfit= minfitdist[i]
        minav= minavdist[i]
        numround= numrounddist[i]
        send(intent, octtraker, cohort, sameserver, avgalgo, fracfit, minfit, minav, numround)
        octtraker=octtraker+cohort
       # time.sleep(timegap)


main()
