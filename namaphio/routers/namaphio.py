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


# DB structure
# DB[0] Meta field & List of Tables
#  - tables: Set, List of all tables
#  - {table}: Hash, Meta Field of each Table
#    - meta: str, Constant meta data like apiversion
#    - header: str, Hash info
#    - types: str, Hash info
#    - geogrid: str, Hash info
#    - mod:{module}: str, Hash info
#
# DB[1] Local Constant Data
#  - {table}: Hash, Contents
#    - header: str, User configure
#    - types: str, Types info used in GeoGrid and Mods
#    - geoGrid: str, Geometry info bound with grids
#
# DB[2] Simulated Data
#  - {table}
#    - {module}: str, module output data


def get_field(db, table: str, field: Union[str, List[str]]):
    res = {}
    for _f in field:
        f = _f.lower()
        if f == 'meta':
            cont = db(0).hgetall(table)
            temp = json.loads(cont.pop(b'meta'))
            temp[b'hashes'] = cont
        elif f in ['header', 'types', 'geogrid']:
            temp = json.loads(db(1).hget(table, f))
        elif f == 'modules':
            temp = {k.decode(): json.loads(v) for k, v in db(2).hgetall(table).items()}
        elif re_mod.match(f):
            f = re_mod.sub('', f)
            cont = db(2).hget(table, f)
            if cont is None:
                raise HTTPException(status_code=404, detail=f"Field not found > {_f}")
            temp = json.loads(cont)
        else:
            raise HTTPException(status_code=404, detail=f"Field not found > {_f}")
        res[f] = temp
    return res


def check_post_que(body: Dict[str, Any]):
    res = []

    for k, v in body.items():
        f = k.lower()
        if re_mod.match(f):
            res.append((2, re_mod.sub('', f), json.dumps(v)))
        elif f in ['header', 'types', 'geogrid']:
            res.append((1, f, json.dumps(v)))
        elif f == 'modules':
            for modk, modv in v.items():
                res.append([2, modk.lower(), json.dumps(modv)])
        elif f == 'meta':
            raise HTTPException(status_code=403, detail=f"DO NOT EDIT META FIELD")
        else:
            raise HTTPException(status_code=404, detail=f"Field not found > {k}")
    return res




@router.get('/tables')
async def list_tables(
    db: Optional[Any] = Depends(connect_database)
):
    """List Tables
      List up all tables on DB

    Returns:
      List[str]: Table names
    """
    return db(0).smembers('tables')


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
        temp = db(0).hgetall(table)
        meta = json.loads(temp.pop(b'meta'))
        meta[b'hashes'] = temp

        cont = {k.decode(): json.loads(v) for k, v in db(1).hgetall(table).items()}
        mods = {k.decode(): json.loads(v) for k, v in db(2).hgetall(table).items()}
        return {'meta': meta, 'modules': mods, **cont}
    return get_field(db, table, field)


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
    que = check_post_que(body)
    for n, field, cont in que:
        db(n).hset(table, field, cont)
        field = f'mod:{field}' if n == 2 else field
        db(0).hset(table, field, hashlib.sha256(cont.encode()).hexdigest())
    return Response(status_code=status.HTTP_200_OK)


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
    if 'meta' in [f.lower() for f in field]:
        raise HTTPException(status_code=403, detail=f"DO NOT EDIT META FIELD")

    res = []
    for _f in field:
        f = _f.lower()
        if f in ['header', 'types', 'geogrid']:
            ap = db(1).hset(table, f, '{}')
            db(0).hset(table, f, '{}')
        elif f == 'modules':
            for i in [i.decode() for i in db(2).hkeys(table)]:
                db(0).hdel(table, f'mod:{i}')
            ap = db(2).delete(table)
        elif re_mod.match(f):
            f = re_mod.sub('', f)
            ap = db(2).hdel(table, f)
            db(0).hdel(table, f'mod:{f}')
        if ap != 0:
            res.append(_f)

    return res
