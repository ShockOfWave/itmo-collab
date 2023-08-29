from fastapi import APIRouter

from . import video, rtc


def init(app):
    router = APIRouter()
    modules = [
        video,
        rtc
    ]
    for modul in modules:
        router.include_router(modul.router)
    app.include_router(router)
