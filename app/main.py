from app.core.configs import settings, tags_metadata

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.db.base import DatabaseManager

from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.0.1',
    docs_url=settings.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# from app.api.v1 import


app.include_router(
    # ROUTE HERE
    prefix=settings.API_V1_STR,
    tags=["Client"]
)


instrumentator = Instrumentator().instrument(app)


@app.on_event('startup')
async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )

    instrumentator.expose(app, include_in_schema=True, should_gzip=True)
    await settings.fetch_timezones()


@app.on_event('shutdown')
async def shutdown():
    await DatabaseManager.stop()
