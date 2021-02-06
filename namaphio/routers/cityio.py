from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
import requests

import yaml

from typing import List, Dict, Any

router = APIRouter(
    prefix='/cityio',
    tags=['compat'],
)

with open('namaphio/config.yml', 'r') as f:
    config = yaml.safe_load(f)['cityio']
host = config['host']
methods = config['methods']


@router.get("/tables/list")
async def list_tables():
    """io_list_tables
      List up whole tables in DB

    Returns:
    List[]
    """
    res = requests.get(f"{host}{methods['ListTables']}")
    return res.json()


@router.get("/table/{table}")
async def get_table(
    table: str
):
    pass


@router.post("/table/update/{table}/{field}")
async def post_table(
    table: str,
    field: str = None
):
    pass


@router.get("/table/clear/{table}/{field}")
async def delete_table(
    table: str,
    field: str = None
):
    pass
