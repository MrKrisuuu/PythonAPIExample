import requests
import json


async def get_game(game):
    try:
        url = "https://steam2.p.rapidapi.com/search/" + game + "/page/1"
        headers = {
            'x-rapidapi-host': "steam2.p.rapidapi.com",
            'x-rapidapi-key': "1f01f8ddd3msh871ef85e63af861p16acd1jsn7e40e8eceae2"
        }
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        first_game = data[0]
        test = first_game["price"]
        if len(test.split('€')) == 3:
            price = test.split('€')[0] + "€ (now: " + test.split('€')[1] + "€)"
        elif len(test.split('€')) == 2:
            price = test.split('€')[0] + '€'
        else:
            price = test
        return (first_game["appId"], first_game["title"], price)
    except:
        return (None, None, None)

