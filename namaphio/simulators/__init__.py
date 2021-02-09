from typing import NamedTuple, Union, List, Dict, Any, Callable
import json
from time import sleep
import traceback

from enum import Enum

import yaml
import re

JSON = Union[Dict[str, Any], List[Any], str, int, float, bool]
Simulator = Callable[[Any], JSON]
re_mod = re.compile('mod:')

with open('namaphio/config.yml', 'r') as f:
    config = yaml.safe_load(f)['simulator']


class Module(NamedTuple):
    name: str = 'Sample'
    in_field: str = 'Types'
    func: Simulator = lambda x: x


class State(Enum):
    Running = 0
    Done = 1
    Cancelled = 2
    Terminated = 3
    Error = 4


class Simulator():
    def __init__(self):
        self.sims = {}
        self.meta = {}

    def setup(self, sims: List[Module]) -> Any:
        self.sims = {s.name: s for s in sims}
        return self.sims.keys()

    def check_update(self, db, table: str):
        temp = db.get_meta_all(table)['hashes']
        res = {f: temp[f] != h for f, h in self.meta.items()}
        return res

    def iter_sim(self, sim_list: List[str], sim_res: Dict[str, List[Any]], db, table):
        try:
            for n in sim_list:
                sim = self.sims[n]
                data = None
                if sim.in_field == 'all':
                    data = db.get_local_all(table)
                else:
                    data = db.get_local(table, [sim.in_field.lower()])[0]
                ret = sim.func(data)
                sim_res[n].append(ret)
                db.set_mod(table, {f'mod:{sim.name.lower()}': sim_res[n]})
            return None
        except Exception as e:
            return e, sim

    def logging(self, db, name: str, state: State, msg: Any):
        cont = {name: {"state": state.name, "msg": msg}}
        log = db.get_temp(['log'])
        db.set_temp({'log': {**(log or {}), **cont}})

    def run(self, id: str, names: List[str], db, table) -> None:
        for i in names:
            if i not in self.sims.keys():
                self.logging(db, i, State.Error, f'ModuleName <{i}> Not Found')
                return

        db.set_mod(table, {k: {} for k in names})

        sim_list = names
        sim_res = {i: [] for i in sim_list}
        chan = db.subscribe_channel(id)

        print(f'Start Running > {sim_list}')
        db.set_temp({id: State.Running.name})
        self.meta = db.get_meta_all(table)['hashes']

        first = True

        for _ in range(config['duration']):
            if len(sim_list) == 0:
                print('No sim left, Done')
                return
            changes = self.check_update(db, table)
            if first:
                changes = {k: True for k in db.get_meta_all(table)['hashes'].keys()}
                first = False
            changes['all'] = True
            cur = [changes[self.sims[s].in_field] and s for s in sim_list]
            err = self.iter_sim(filter(lambda x: x is not False, cur), sim_res, db, table)
            self.meta = db.get_meta_all(table)['hashes']

            if err is not None:
                e, sim = err
                print(f'Unexpected Error occured: {e.args}')
                db.set_temp({id: State.Error.name})
                self.logging(db, sim.name, State.Error, [str(type(e)), e.args, traceback.format_exc()])
                return

            msg = chan.get_message()
            if (msg is not None) and (msg['data'] == State.Cancelled.name):
                print(f'Cancelled: {id} > {sim_list}')
                db.set_temp({id: State.Cancelled.name})
                return

            sleep(1 / config['fps'])

        print(f'Done > {sim_list}')
        db.set_temp({id: State.Done.name})

    def stop(self, db, ids: List[str]) -> bool:
        for i in ids:
            print(f'Recieve termination signal > {i}')
            db.publish_msg(i, State.Cancelled.name)
        return True

    def get_jobs(self, db):
        job = db.get_temp_all()
        log = {}
        if 'log' in job.keys():
            log = job.pop('log')
        return {'state': {k: v for k, v in job.items()}, 'log': log}
