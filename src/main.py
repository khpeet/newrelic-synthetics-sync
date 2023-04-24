import requests
import json
import logging

def main():
    print('nice')
    monitors = json.loads('monitors.json');
    print(monitors);

    # Read filenames in from files.json (array)
    # For each file:
        # Entitysearch to determine if existing or not - if yes -- read script + update call -- if no, create new monitor with default inputs




def getMonitor(name):
    GRAPHQL_API = 'https://api.newrelic.com/graphql'
    vars = {"monitorName":  name}
    gql = """
      query($monitorName: String!){
        actor {
          entitySearch(queryBuilder: {domain: SYNTH, name: $monitorName}) {
            results {
              entities {
                ... on SyntheticMonitorEntityOutline {
                  name
                  monitorId
                  guid
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
                monitorId = resp['data']['actor']['entitySearch']['results']['entities'][0]['guid']
                return monitorId
            else:
                print("No matching id found for monitor: " + name + ' Skipping...')
        else:
            print("Error retrieving ID for monitor: " + name + ' Skipping...')
            print(resp['errors'])
    except requests.exceptions.RequestException as e:
        print("Error retrieving ID for monitor: " + name + ' Skipping...')
        print(e)
        return 'none'

    return 'none'


if __name__ == '__main__':
    main()
