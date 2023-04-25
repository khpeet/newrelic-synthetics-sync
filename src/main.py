import requests
import json
import re
import sys
import os
from actions_toolkit import core

GRAPHQL_API = 'https://api.newrelic.com/graphql'
GRAPHQL_KEY =  os.getenv('NEW_RELIC_API_KEY')
WORKSPACE = os.getenv('GITHUB_WORKSPACE')

def main():
    fileNames = readAndParseFile()
    print(fileNames)

    acct = core.get_input('accountId', required=False)
    print(acct)

    # n = len(sys.argv)
    # print(n)
    # print(sys.argv)
    # core.get_input('name', required=False)

    # for monitor in fileNames:
    #     m = getMonitor(monitor['name'])
    #     if (m != 'none'):
    #         updateMonitor(m, monitor['script'])
    #     else:
    #         createMonitor(monitor, monitor['script'])


def readAndParseFile():
    monitorList = None
    formatted = []
    with open("monitors.json", "r") as f:
        monitorList = json.load(f)

    pattern = r"[^/]*(?=\.[^/]*$)" #remove file path and .js extension
    if (len(monitorList) > 0):
        for mon in monitorList:
            script = WORKSPACE + '/' + mon
            fileReader = open(script, 'r')
            scriptContent = fileReader.read()
            formattedMonitor = re.search(pattern, mon)
            if formattedMonitor:
                formatted.append({'name': formattedMonitor.group(0), 'script': scriptContent })
    else:
        print('No monitors found in file. Exiting')
        sys.exit(1)

    return formatted


def getMonitor(name):
    vars = {"monitorName":  name}
    gql = """
        query ($monitorName: String!) {
          actor {
            entitySearch(queryBuilder: {domain: SYNTH, name: $monitorName}) {
              results {
                entities {
                  ... on SyntheticMonitorEntityOutline {
                    name
                    monitorId
                    monitorType
                    guid
                    account {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
    """
    h = {'Content-Type': 'application/json', 'API-Key': GRAPHQL_KEY}
    try:
        r = requests.post(GRAPHQL_API, headers=h, json={'query': gql, 'variables': vars})
        resp = r.json()
        if (r.status_code == 200):
            if (len(resp['data']['actor']['entitySearch']['results']['entities']) > 0):
                monitorResp = resp['data']['actor']['entitySearch']['results']['entities'][0]
                return monitorResp
            else:
                print("No matching id found for monitor: " + name + '. Creating new monitor...')
        else:
            print("Error retrieving monitor: " + name + '. Skipping...')
            print(resp['errors'])
    except requests.exceptions.RequestException as e:
        print("Error retrieving monitor: " + name + ' Skipping...')
        print(e)
        return 'none'

    return 'none'


def updateMonitor(monitor, script):
        vars = {"guid": monitor['guid'], "script": script}
        type = None

        if (monitor['monitorType'] == 'SCRIPT_BROWSER'):
            type = 'syntheticsUpdateScriptBrowserMonitor'
        elif (monitor['monitorType'] == 'SCRIPT_API'):
            type = 'syntheticsUpdateScriptApiMonitor'


        if (type != None):
            gql = f"""
                mutation ($guid: EntityGuid!, $script: String!) {{
                  {type}(guid: $guid, monitor: {{script: $script}}) {{
                    errors {{
                      description
                      type
                    }}
                    monitor {{
                      guid
                      name
                      status
                    }}
                  }}
                }}
            """
            h = {'Content-Type': 'application/json', 'API-Key': GRAPHQL_KEY}
            try:
                r = requests.post(GRAPHQL_API, headers=h, json={'query': gql, 'variables': vars})
                resp = r.json()
                if (resp['data'][type]['errors']):
                    print("Error updating monitor: " + monitor['name'] + 'Skipping...')
                    print(resp['errors'])
                else:
                    print("Successfully updated monitor: " + resp['data'][type]['monitor']['name'] + ". Monitor is currently " + resp['data'][type]['monitor']['status'])
            except requests.exceptions.RequestException as e:
                print("Error updating monitor: " + monitor['name'] + ' Skipping...')
                print(e)
        else:
            print('Type for monitor:' + monitor['name'] + 'is ' + monitor['monitorType'] + ". Scripted API or Browser are only accepted types. Skipping update...")

def createMonitor(monitor, script):
        vars = {"account": 1, "locations": locs, "name": monitor['name'], "interval": intval, "script": script, "status": status}
        type = None

        #only proceed if inputs defined in action.yml exist in workflow yaml*** print error if any are missing***

        #locations example -- {private: [{guid: ""}], public: ['LOCATION_1', 'LOCATION_2']}
        #runtime -- {runtimeType: "", runtimeTypeVersion: ""} -- need type/version inputs here

        if (monitor['monitorType'] == 'SCRIPT_BROWSER'):
            type = 'syntheticsCreateScriptBrowserMonitor'
        elif (monitor['monitorType'] == 'SCRIPT_API'):
            type = 'syntheticsCreateScriptApiMonitor'


        if (type != None):
            gql = f"""
                mutation($account: Int!, $locations: SyntheticsScriptedMonitorLocationsInput!, $name: String!, $interval: SyntheticsMonitorPeriod!, $script: String!, $status: SyntheticsMonitorStatus! ) {{
                  {type}(accountId: $account, monitor: {{locations: $locations, name: $name, period: $interval, runtime: {{runtimeType: "", runtimeTypeVersion: ""}}, script: $script, status: $status}}) {{
                    errors {{
                      description
                      type
                    }}
                    monitor {{
                      guid
                      name
                      status
                    }}
                  }}
                }}
            """
            print(gql)
        #     h = {'Content-Type': 'application/json', 'API-Key': GRAPHQL_KEY}
        #     try:
        #         r = requests.post(GRAPHQL_API, headers=h, json={'query': gql, 'variables': vars})
        #         resp = r.json()
        #         if (resp['errors']):
        #             print("Error creating monitor: " + monitor['name'] + 'Skipping...')
        #             print(resp['errors'])
        #         else:
        #             print("Successfully created new monitor: " + resp['data'][type]['monitor']['name'] + ". Monitor is currently " + resp['data'][type]['monitor']['status'])
        #     except requests.exceptions.RequestException as e:
        #         print("Error creating monitor: " + monitor['name'] + ' Skipping...')
        #         print(e)
        # else:
        #     print('Type for monitor:' + monitor['name'] + 'is ' + monitor['monitorType'] + ". Scripted API or Browser are only accepted types. Skipping create...")

if __name__ == '__main__':
    main()
