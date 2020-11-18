import requests
from pymongo import MongoClient
import sys
import time
import datetime

#Connect to the DB (ip with default port)
DB = sys.argv[1]
#Connecto to the ONOS
CTRL = sys.argv[2]
#Delay (default 10s)
DELAY = 10
if(sys.argv.__len__()>3):
    DELAY = int(sys.argv[3])

client = MongoClient(DB,27017)
db = client["outpow"]
col=db["outpow1"]
lastUpdated = 0
while True:
    if lastUpdated +DELAY< time.time():
        n = datetime.datetime.now() - datetime.timedelta(0,DELAY,0,0,0,1) #Change clock on machines!!!!!!
        print(n.time(), n.date())
        powerUpdate = dict()
        print("update")
        for record in col.find({"timestamp":{"$gt":n}}):
            if str(record["sensor"]) in powerUpdate.keys():
                powerUpdate[str(record["sensor"])] = float((powerUpdate[record["sensor"]]+record["power"])/2)
            else:
                powerUpdate[str(record["sensor"])] = record["power"]
        print(powerUpdate)
        lastUpdated = time.time()
        #send the rq with gathered data to the controller
        x = requests.post("http://{}:8181/onos/rnn/SRE/energy".format(CTRL),json=powerUpdate,auth=("karaf","karaf"))
        print(x.text)