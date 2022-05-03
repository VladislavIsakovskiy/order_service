# type: ignore[attr-defined]
import os
from os.path import join as path_join

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from logger_config import logger

from order_service.endpoints import items, orders
from order_service.errors import APIError


def create_app() -> FastAPI:
    logger.info("Starting order service app!")
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


@order_app.middleware("http")
async def request_log(request: Request, call_next):
    """
    Global exception handler for catching non API errors.
    ALso catch, sort and write uvicorn output and critical errors to log
    :param request: Request
    :param call_next: call_next
    :return: JSONResponse
    """
    try:
        response: Response = await call_next(request)
        if response.status_code < 400:
            logger.info(f"{request.method} {request.url} Status code: {response.status_code}")
        else:
            logger.warning(f"{request.method} {request.url} Status code: {response.status_code}")
        return response
    except Exception as exc:  # noqa # pylint: disable=broad-except
        logger.exception(str(exc))
        return JSONResponse(
            content={"message": "Something went wrong!"},
        )


@order_app.exception_handler(APIError)
def api_exception_handler(_request: Request, exc: APIError) -> JSONResponse:
    """
    Exception handler for catching API errors
    :param _request: Request
    :param exc: APIError
    :return: JSONResponse
    """
    logger.warning(exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
