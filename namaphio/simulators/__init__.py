from typing import NamedTuple, Union, List, Dict, Any, Callable
import json
from time import sleep
import traceback

from enum import Enum

import yaml

JSON = Union[Dict[str, Any], List[Any], str, int, float, bool]
Simulator = Callable[[Any], JSON]

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
        temp = db(0).hgetall(table)
        res = {f: self.meta[f] != h for f, h in temp.items()}
        self.meta = temp
        return res

    def run(self, names: List[str], db, table) -> None:
        for i in names:
            if i not in self.sims.keys():
                self.log.append(
                    {
                        i: {
                            "state": State.Error.name,
                            "msg": f'ModuleName <{i}> Not Found'
                        }
                    }
                )
                return

        for i in names:
            self.jobs[i] = State.Running

        sim_list = names
        sim_res = {i: [] for i in sim_list}
        print(f'Start Running > {sim_list}')
        try:
            for n in sim_list:
                sim = self.sims[n]
                data = "[]" if sim.in_field is None else db(1).hget(table, sim.in_field.lower())
                ret = sim.func(json.loads(data))
                sim_res[n].append(ret)
                db(2).hset(table, sim.name.lower(), json.dumps(sim_res[n]))
                db(0).hset(table, f'mod:{sim.name.lower()}', len(sim_res[n]))
                self.meta = db(0).hgetall(table)
            sleep(1 / config['fps'])
            for _ in range(config['duration'] - 1):
                if len(sim_list) == 0:
                    return
                changes = self.check_update(db, table)
                for n in sim_list:
                    sim = self.sims[n]
                    if sim.in_field is None:
                        data = '[]'
                    elif changes[sim.in_field.lower().encode()]:
                        data = db(1).hget(table, sim.in_field.lower())
                    else:
                        continue
                    ret = sim.func(json.loads(data))
                    sim_res[n].append(ret)
                    db(2).hset(table, sim.name.lower(), json.dumps(sim_res[n]))
                    db(0).hset(table, f'mod:{sim.name.lower()}', len(sim_res[n]))

                    if self.jobs[n] == State.Cancelled:
                        sim_list.remove(n)
                        print(f'Cancelled: {n} > Left: {sim_list}')

                sleep(1 / config['fps'])

        except Exception as e:
            print(f'Unexpected Error occured: {e.args}')
            for i in sim_list:
                self.jobs[i] = State.Terminated
            self.jobs[sim.name] = State.Error
            self.log.append({sim.name: {"state": State.Error.name, "msg": [str(type(e)), e.args, traceback.format_exc()]}})
            return

        print(f'Done > {sim_list}')
        for i in sim_list:
            self.jobs[i] = State.Done

    def stop(self, names: List[str]) -> bool:
        print(f'Recieve termination signal > {names}')
        for i in names:
            if i not in self.jobs.keys() or self.jobs[i] != State.Running:
                return False
        for i in names:
            self.jobs[i] = State.Cancelled
        return True

    def get_jobs(self):
        return {'state': {k: v.name for k, v in self.jobs.items()}, 'log': self.log}
