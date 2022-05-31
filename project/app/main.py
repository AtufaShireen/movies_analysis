from typing import Union
from utils import *
from fastapi.responses import FileResponse,StreamingResponse,Response, HTMLResponse
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates/")
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/top_movies")
def top_n_movies(n=10,year=None,genre=None,plot_key=None):
    print("-----------------here")
    # year = kwargs.get("year")
    # genre = kwargs.get("genre")
    # plot_key = kwargs.get("plot_key")

    if year:

        movies = top_n_movs(year=year,n=n)
        return [i['title'] for i in movies]
    elif genre:
        movies = top_n_movs(genre=genre,n=n)
        return [i['title'] for i in movies]
    elif plot_key:
        movies = top_n_movs(plot_key=plot_key,n=n)
        return [i['title'] for i in movies]
    else:
        movies = top_n_movs(n=n)
        return [i['title'] for i in movies]
