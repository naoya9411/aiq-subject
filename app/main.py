import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import router


app = FastAPI()

allow_origins = [
    os.environ['ALLOW_ORIGIN']
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router_v1 = APIRouter(prefix='/v1', tags=['API v1'])


@app.get('/')
def read_root():
    return {'healthcheck': 'success'}


router_v1.include_router(router)

app.include_router(router_v1)
