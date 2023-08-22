import asyncio

from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles



def init_app(app):
    from .routers import init as init_routers

    app.mount('/static', StaticFiles(directory='src/static'), name='static')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_routers(app)

    @app.on_event('shutdown')
    async def shutdown_event():
        from src.rtc import pcs

        coros = [pc.close() for pc in pcs]
        await asyncio.gather(*coros)
        pcs.clear()


