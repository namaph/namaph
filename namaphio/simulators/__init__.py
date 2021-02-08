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
        self.jobs = {}
        self.log = []
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
                if sim.in_field is None:
                    data = db.get_local_all(table)
                else:
                    data = db.get_local(table, [sim.in_field.lower()])[0]
                ret = sim.func(data)
                sim_res[n].append(ret)
                db.set_mod(table, {f'mod:{sim.name.lower()}': sim_res[n]})
            return None
        except Exception as e:
            return e, sim

    def set_state(self, sim_list: List[str], state: State):
        for i in sim_list:
            self.jobs[i] = state

    def logging(self, name: str, state: State, msg: Any):
        self.log.append({name: {"state": state.name, "msg": msg}})

    def run(self, names: List[str], db, table) -> None:
        for i in names:
            if i not in self.sims.keys():
                self.logging(i, State.Error, f'ModuleName <{i}> Not Found')
                return

        self.set_state(names, State.Running)

        db.set_mod(table, {k: {} for k in names})

        sim_list = names
        sim_res = {i: [] for i in sim_list}

        print(f'Start Running > {sim_list}')
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
                self.set_state(sim_list, State.Terminated)
                self.jobs[sim.name] = State.Error
                self.logging(sim.name, State.Error, [str(type(e)), e.args, traceback.format_exc()])
                return

            for sim in sim_list:
                state = self.jobs[sim]
                if state == State.Cancelled:
                    sim_list.remove(sim)
                    print(f'Cancelled: {sim} > Left: {sim_list}')

            sleep(1 / config['fps'])

        print(f'Done > {sim_list}')
        self.set_state(sim_list, State.Done)

    def stop(self, names: List[str]) -> bool:
        print(f'Recieve termination signal > {names}')
        for i in names:
            if i not in self.jobs.keys() or self.jobs[i] != State.Running:
                return False
        self.set_state(names, State.Cancelled)
        return True

    def get_jobs(self):
        return {'state': {k: v.name for k, v in self.jobs.items()}, 'log': self.log}
