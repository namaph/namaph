import redis
from starlette.requests import Request
import yaml

import os

from typing import Dict, List, Any, Union, Iterable
import hashlib

import json

# DB structure
# DB[1] Local Constant Data
#  - {table}: Hash, Contents
#    - header: str, User configure
#    - types: str, Types info used in GeoGrid and Mods
#    - geoGrid: str, Geometry info bound with grids
#
# DB[2] Simulated Data
#  - {table}
#    - {module}: str, module output data


class NamaphDB():
    """
DB[0] Meta field & List of Tables
 - tables: Set, List of all tables
 - {table}: Hash, Meta Field of each Table
   - meta: str, Constant meta data like apiversion
   - header: str, Hash info
   - types: str, Hash info
   - geogrid: str, Hash info
   - mod:{module}: str, Hash info
DB[1] Local Constant Data
 - {table}: Hash, Contents
   - header: str, User configure
   - types: str, Types info used in GeoGrid and Mods
   - geoGrid: str, Geometry info bound with grids

DB[2] Simulated Data
 - {table}
   - {module}: str, module output data
DB[3] Fetched Data
  - {table}: str, fetched data from cityio, raw json
    """

    def __init__(self, host: str, port: int):
        self._db = {"meta": 0, "local": 1, "mod": 2, "remote": 3}
        self.pool = {
            k: redis.ConnectionPool(
                host=host, port=port, db=v, decode_responses=True
            )for k, v in self._db.items()
        }

    def get_tables(self) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        return r.smembers('tables')

    def get_meta_all(self, table: str) -> Dict[str, Any]:
        r = redis.StrictRedis(connection_pool=self.pool["meta"])

        raw = r.hgetall(table)
        if raw is None:
            return None

        meta = {k: raw.pop(k) for k in ['apiv', 'id', 'timestamp']}
        data = {**meta, 'hashes': {**raw}}
        return data

    def get_meta(self, table: str, whre: Iterable[str]) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()
        for f in where:
            pipe.hget(table, f)
        data = pipe.execute()

        return data

    def get_local_all(self, table: str) -> Dict[str, Any]:
        r = redis.StrictRedis(connection_pool=self.pool['local'])
        raw = r.hgetall(table)
        data = {k: json.loads(v) for k, v in raw.items()}
        return data

    def get_local(self, table: str, where: Iterable[str]) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool['local'])
        pipe = r.pipeline()
        for f in where:
            pipe.hget(table, f)
        data = [None if i is None else json.loads(i) for i in pipe.execute()]
        return data

    def set_local(self, table: str, cont: Dict[str, any]) -> List[int]:
        r = redis.StrictRedis(connection_pool=self.pool['local'])
        r_m = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()
        pipe_m = r_m.pipeline()

        for k, v in cont.items():
            if k in ('header', 'types', 'geogrid'):
                c = json.dumps(v)
                pipe.hset(table, k, c)
                pipe_m.hset(table, k, hashlib.sha256(c.encode()).hexdigest())

        data = pipe.execute()
        d_m = pipe_m.execute()
        return data

    def del_local(self, table: str, where: Iterable[str]) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool['local'])
        r_m = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()
        pipe_m = r_m.pipeline()

        for f in where:
            if f in ('header', 'types', 'geogrid'):
                pipe.hset(table, f, '{}')
                pipe_m.hset(table, f, '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a')

        data = pipe.execute()
        d_m = pipe_m.execute()
        return data

    def get_mod_all(self, table: str) -> Dict[str, Any]:
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        raw = r.hgetall(table)
        data = {k: json.loads(v) for k, v in raw.items()}
        return data

    def get_mod(self, table: str, where: Iterable[str]) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        pipe = r.pipeline()

        for f in where:
            pipe.hget(table, f)
        data = [None if i is None else json.loads(i) for i in pipe.execute()]
        return data

    def set_mod(self, table: str, cont: Dict[str, any]) -> List[int]:
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        r_m = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()
        pipe_m = r_m.pipeline()

        for k, v in cont.items():
            c = json.dumps(v)
            pipe.hset(table, k, c)
            pipe_m.hset(table, k, hashlib.sha256(c.encode()).hexdigest())
        data = pipe.execute()
        d_m = pipe_m.execute()
        return data

    def del_mod(self, table: str, where: Iterable[str]) -> List[str]:
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        r_m = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()
        pipe_m = r_m.pipeline()

        for f in where:
            pipe.hdel(table, f)
            pipe_m.hdel(table, f)
        data = pipe.execute()
        d_m = pipe_m.execute()
        return data

    def get_temp_all(self):
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        raw = r.hgetall('temp')
        data = {k: json.loads(v) for k, v in raw.items()}
        return data

    def get_temp(self, where: Iterable[str]) -> List[Any]:
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()

        for f in where:
            pipe.hget('temp', f)
        data = [None if i is None else json.loads(i) for i in pipe.execute()]
        return data

    def set_temp(self, cont: Dict[str, Any]) -> List[int]:
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        pipe = r.pipeline()

        for k, v in cont.items():
            c = json.dumps(v)
            pipe.hset('temp', k, c)
        data = pipe.execute()
        return data

    def clear_cache(self):
        r = redis.StrictRedis(connection_pool=self.pool["meta"])
        r.delete('temp')

    def publish_msg(self, channel: str, msg: str):
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        r.publish(channel, msg)

    def subscribe_channel(self, channel: str):
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        ps = r.pubsub()

        ps.subscribe(channel)
        return ps

    def get_channels(self):
        r = redis.StrictRedis(connection_pool=self.pool['mod'])
        return r.pubsub_channels()


def register_db(host: str, port: int):
    db = NamaphDB(host, port)

    def get_database():
        return db
    return get_database


with open('namaphio/config.yml', 'r') as f:
    config = yaml.safe_load(f)['redis']

get_database = register_db(
    host=os.environ.get('REDISHOST', config['host']),
    port=os.environ.get('REDISPORT', config['port']),
)
