import json

from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning

def getRoundRobinStandings(id):

    response = requests.get(f"https://api.score7.io/tournaments/{id}/roundRobinGroups")
    data = response.json()
    #print(data)
    field_value = data[0]["id"]
    #print(field_value)

    url = "https://api.score7.io/roundRobinGroups/" + str(field_value) + "/standing"
    response = requests.get(url)
    data = response.json()
    field_value = data["id"]
    #print(field_value)

    url = "https://api.score7.io/standings/" + str(field_value) + "/standingEntries"
    response = requests.get(url)
    data = response.json()
    #print(data)
    lista = []

    for k in data:
            lista.append(k["participant"]["name"])
            lista.append(str(int(k["points"])))


    return lista

def clubscore_api_scraper(path,target_url):
    base_url = "https://clubscorestats.herokuapp.com/"
    url = base_url + path


    payload = json.dumps({
        "url": target_url
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()