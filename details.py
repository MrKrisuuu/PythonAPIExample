import requests
import json


async def get_details(id):
    try:
        url = "https://steam2.p.rapidapi.com/appDetail/" + id
        headers = {
            'x-rapidapi-host': "steam2.p.rapidapi.com",
            'x-rapidapi-key': "1f01f8ddd3msh871ef85e63af861p16acd1jsn7e40e8eceae2"
            }
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        return data["description"]
    except:
        return None