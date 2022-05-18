from fastapi import FastAPI
import uvicorn
from game import get_game
from details import get_details
from reviews import get_reviews


app = FastAPI()


@app.get("/{game}")
async def get_user(game):
    (id, title, price) = await get_game(game)
    if (id, title, price) == (None, None, None):
        error = {"message": "Game not found"}
        return error
    description = await get_details(id)
    if description == None:
        description = "Couldn't find description"
    (positive, negative) = await get_reviews(id)
    if (positive, negative) == (None, None):
        a_reviews = "Couldn't find"
        p_reviews = "Couldn't find"
        n_reviews = "Couldn't find"
    else:
        positive_percent = " (" + str(round(100 * positive / (positive + negative), 2)) + "%)"
        negative_percent = " (" + str(round(100 * negative / (positive + negative), 2)) + "%)"
        a_reviews = positive + negative
        p_reviews = str(positive) + positive_percent
        n_reviews = str(negative) + negative_percent
    result = {"game": title,
              "price": price,
              "description": description,
              "a_reviews": a_reviews,
              "p_reviews": p_reviews,
              "n_reviews": n_reviews}
    return result


uvicorn.run(app, host="127.0.0.1", port=8000)