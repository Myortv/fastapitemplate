from app.core.configs import settings, tags_metadata

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from plugins.controllers import DatabaseManager

# from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.0.1',
    docs_url=settings.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

# create CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# start database pool
@app.on_event('startup')
async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )


# startup prometheus
#
# instrumentator = Instrumentator().instrument(app)


# generate microservice-microsevice jwt token
#
# settings.api_token = api_token_manager.encode(
#     {
#         'service_name': app.title,
#     }
# )


# shutdown database pool and aiohttp session
@app.on_event('shutdown')
async def shutdown():
    await DatabaseManager.stop()
    await settings.aiohttp_session.close()


# load routers
# make sure to start plugins before importing routers
from app.api.v1 import rename


# bind routers
app.include_router(
    router=rename.router,
    prefix=settings.API_V1_STR,
    tags=["rename"]
)
