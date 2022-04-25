from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
from game import get_game
from details import get_details
from reviews import get_reviews
import starlette.status as status
from starlette.exceptions import HTTPException


app = FastAPI()
templates = Jinja2Templates("templates/")
error = ""


@app.get("/")
async def welcome(request: Request):
    return templates.TemplateResponse('hi.html', context={'request': request})


@app.get("/form")
async def view_form(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request})


@app.post("/form")
async def calculate_form(request: Request, game: str = Form(...)):
    (id, title, price) = await get_game(game)
    if (id, title, price) == (None, None, None):
        return RedirectResponse(url='/error/game', status_code=status.HTTP_302_FOUND)
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
    return templates.TemplateResponse('result.html', context={'request': request,
                                                              'game': title,
                                                              'price': price,
                                                              'description': description,
                                                              'a_reviews': a_reviews,
                                                              'p_reviews': p_reviews,
                                                              'n_reviews': n_reviews})


@app.exception_handler(HTTPException)
async def my_custom_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse(url='/error/page')
    else:
        return RedirectResponse(url='/error/other')


@app.get("/error/game")
async def error(request: Request):
    error = "Game not found"
    return templates.TemplateResponse('error.html', context={'request': request, 'error': error})


@app.get("/error/page")
async def error(request: Request):
    error = "Page not found"
    return templates.TemplateResponse('error.html', context={'request': request, 'error': error})


@app.get("/error/other")
async def error(request: Request):
    error = "Other error"
    return templates.TemplateResponse('error.html', context={'request': request, 'error': error})


uvicorn.run(app, host="127.0.0.1", port=8000)