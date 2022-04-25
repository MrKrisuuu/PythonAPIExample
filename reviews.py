import requests
import json


async def get_reviews(id):
    try:
        url = "https://steam2.p.rapidapi.com/appReviews/" + id +"/limit/40/*"
        headers = {
            'x-rapidapi-host': "steam2.p.rapidapi.com",
            'x-rapidapi-key': "1f01f8ddd3msh871ef85e63af861p16acd1jsn7e40e8eceae2"
            }
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        reviews = data["query_summary"]
        return (reviews["total_positive"], reviews["total_negative"])
    except:
        return (None, None)