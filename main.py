import uvicorn as uvicorn
from fastapi import FastAPI, Request

from src import init_app
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title='ITMO Collab',
    description = 'API',
    docs_url = '/docs',
)

init_app(app)

templates = Jinja2Templates(directory="src/static/html/")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=5555,
        reload=True,
    )