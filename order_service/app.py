# type: ignore[attr-defined]
import os
from os.path import join as path_join

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from order_service.endpoints import items, orders


def create_app() -> FastAPI:
    app = FastAPI(
        title="Order service app",
        description="API for order service app",
    )

    return app


order_app = create_app()

current_dir = os.path.dirname(os.path.abspath(__file__))
order_app.mount(
    "/static",
    StaticFiles(directory=path_join(current_dir, "..", "static")),
    name="static",
)

order_app.include_router(orders.router, prefix="/v1")
order_app.include_router(items.router, prefix="/v1")
