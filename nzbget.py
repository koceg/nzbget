#!/usr/bin/python3
import requests
import json
import sys

def sequence():
    number=0
    while True:
        number+=1
        yield number

try:
    url='http://{}:{}@{}:6789/jsonrpc'.format(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3])

    jsonHeader = {'content-type': 'application/json'}
    
    id=sequence()
    
    payload = {
            "method": "status",
            "jsonrpc": "2.0",
            "id":next(id),
        }

    response = requests.post(
            url,
            data=json.dumps(payload),
            headers=jsonHeader
            ).json()

    if response['result']['ResumeTime']:
        quit()

    payload['method']='listgroups'
    payload['params']={"NumberOfLogEntries":0}
    payload['id']=next(id)

    response = requests.post(
            url,
            data=json.dumps(payload),
            headers=jsonHeader
            ).json()

    if len(response['result']) != 0:
        sample=[]# list of ids to process
        remove=[]

        for queuedFile in response['result']:
            sample.append(queuedFile['NZBID']) #get files in queue for download

        for nzbId in sample:
            #use generator
            payload['method']='listfiles'
            payload['params']={'IDFrom':0,'IDTo':0,'NZBID':nzbId}
            payload['id']=next(id)
            response=None
            response = requests.post(
                    url,
                    data=json.dumps(payload),
                    headers=jsonHeader
                    ).json()


            for article in response['result']:
                if nzbId != article['NZBID']:
                    continue
                if article['Subject'].lower().find('sample')!=-1 or  \
                   article['Filename'].lower().find('sample')!=-1:

                    remove.append(article['ID'])#article ID from file 
    
        if len(remove)!=0:

            payload['method']='editqueue'
            payload['params']=['FileDelete','',remove]
            payload['id']=next(id)

            response = requests.post(
                    url,
                    data=json.dumps(payload),
                    headers=jsonHeader
                    ).json()


        payload['method']='resumedownload'
        payload['params']=''
        payload['id']=next(id)

        response = requests.post(
                url,
                data=json.dumps(payload),
                headers=jsonHeader
                ).json()
    else:

        payload['method']='pausedownload'
        payload['params']=''
        payload['id']=next(id)

        requests.post(
                url,
                data=json.dumps(payload),
                headers=jsonHeader
                ).json()

except Exception as e:
    print("ERROR", e)
