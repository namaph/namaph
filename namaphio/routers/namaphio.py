from fastapi import APIRouter
from fastapi import Query, Path, Depends, Response, status, Body, HTTPException

from typing import List, Dict, Any, Optional, Union, Callable
from fastapi.responses import ORJSONResponse

import hashlib
import re
import json
from ..dependencies import connect_database

router = APIRouter(
    prefix="",
    tags=[],
    default_response_class=ORJSONResponse,
)

re_mod = re.compile('mod:')


@router.get('/tables')
async def list_tables(
    db: Optional[Any] = Depends(connect_database)
):
    """List Tables
      List up all tables on DB

    Returns:
      List[str]: Table names
    """
    return db.get_tables()


@router.get('/table/{table}')
async def get_table(
    table: Optional[str] = Path(..., title="Table name in DB", example='roppongi'),
    field: Optional[List[str]] = Query(None, title="Field names in Table", example=['geogrid', 'modules', 'mod:indicator']),
    db: Optional[Any] = Depends(connect_database)
):
    """Get Table
      Get all fields on the table

    Args:
      table(str): Table name
      field(List[str]): Field names in Table. Default to None.

    Returns:
      Dict[str, Any]: Table fiels specified in `field` argument. If field was None, return all of the fields.
    """
    if field is None:
        meta = db.get_meta_all(table)
        local = db.get_local_all(table)
        mod = db.get_mod_all(table)
        return {"meta": meta, "mod": mod, **local}
    else:
        l_meta = []
        l_local = []
        l_mod = []
        f_mods = False

        for _f in field:
            f = _f.lower()
            if f == 'meta':
                l_meta.append(f)
            elif f in ('header', 'geogrid', 'types'):
                l_local.append(f)
            elif f == 'modules':
                f_mods = True
            elif re_mod.match(f):
                l_mod.append(f)

        meta = {} if l_meta == [] else {"meta": db.get_meta_all(table)}
        local = {} if l_local == [] else {k: v for k, v in zip(l_local, db.get_local(table, l_local))}

        if f_mods:
            mod = {'mods': db.get_mod_all(table)}
        else:
            mod = {} if l_mod == [] else {k: v for k, v in zip(l_mod, db.get_mod(table, l_mod))}
    return {**meta, **local, **mod}


@router.post('/table/{table}')
async def post_table(
    table: Optional[str] = Path(..., title="Table name in DB", example='roppongi'),
    body: Optional[Dict[str, Any]] = Body(..., title="Content", example={'Mod:Test1': {'value': 1}, 'Mod:Test2': [2]}),
    db: Optional[Any] = Depends(connect_database)
):
    """Post Table
      Post body contents on the table.
      Body should be a dict object, and its top level keys set to the Field on the Table.

    Args:
      table(str): Table name
      body(Dict[str, Any]): Pair of fieldName and its content

    Returns:
        None: Response 200
        str: Response 403
        str: Response 404
    """
    local = {}
    mod = {}

    for _k, v in body.items():
        k = _k.lower()
        if k in ('header', 'geogrid', 'types'):
            local[k] = v
        elif re_mod.match(k):
            mod[k] = v

    db.set_local(table, local)
    db.set_mod(table, mod)

    return [*local.keys(), *mod.keys()]


@router.delete('/table/{table}')
async def delete_table(
    table: Optional[str] = Path(..., title="Table name in DB", example='roppongi'),
    field: Optional[List[str]] = Query(..., title="Field names in Table", example=['Mod:Test1', 'Mod:Test2']),
    db: Optional[Any] = Depends(connect_database)
):
    """Delete Table
      Delete fields on the table

    Args:
      table(str): Table name
      field(List[str]): Field names on Table.

    Returns:
      Dict[str, Any]: Table fiels specified in `field` argument. If field was None, return all of the fields.
    """
    local = []
    mod = []

    for _k in field:
        k = _k.lower()
        if k in ('header', 'geogrid', 'types'):
            local.append(k)
        elif re_mod.match(k):
            mod.append(k)

    db.del_local(table, local)
    db.del_mod(table, mod)

    return [*local, *mod]
