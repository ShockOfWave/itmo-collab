from fastapi import APIRouter

from . import media


def init(app):
    router = APIRouter()
    modules = [
        media
    ]
    for modul in modules:
        router.include_router(modul.router)
    app.include_router(router)
