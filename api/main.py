from dotenv import load_dotenv

load_dotenv()

import uvicorn as uvicorn
from fastapi import FastAPI

from api.src import init_app
from fastapi.templating import Jinja2Templates

from api.src.models import check_models, init_models

check_models()
segmentation_model, classification_model = init_models()

app = FastAPI(
    title="ITMO Collab",
    description="API",
    docs_url="/docs",
)

init_app(app)

templates = Jinja2Templates(directory="src/static/html/")


# @app.get('/')
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5556,
        reload=True,
    )
