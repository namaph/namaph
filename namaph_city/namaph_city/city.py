import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Tuple, Any, NamedTuple, Callable

from Ecosystem.types import Ecosystem
from Ecosystem.temp import setup
from Ecosystem.utils import mult_by_layer, default_ecosystem, set_random, set_scale, animate
from Ecosystem.operations import calc_energy, get_neighbors
# from Ecosystem.simulators import grow

from os.path import dirname, join
import json

np.set_printoptions(suppress=True)


def grow(
  system: Ecosystem,
  plants: pd.DataFrame
) -> Ecosystem:
    res, spc, ene = system.resource, system.species, system.energy
    rel = plants.filter(regex='p')
    N = spc
    K_ene = res + mult_by_layer(N, plants.e)
    K_ene[K_ene.round(4) == 0] = 1e-4
    K_num = mult_by_layer(K_ene, 1/plants.e)

    # Logistic Function w/ plant interaction ...
    # plant.rのhetelogeneity | fraction(?)
    # ... 同じ状況で経過するとneg e.g. 自分でやられるアレロパシー
    interaction = np.array([mult_by_layer(N, rel.iloc[i]).sum(axis=0) for i in range(len(spc))])
    mask = np.ones_like(spc)
    mask[spc == 0] = 0
    interaction *= mask
    logistic = mult_by_layer(N * (1 - (N - interaction) / K_num), plants.r)

    n_spc = N + logistic
    n_spc[n_spc < 1e-4] = 0
    n_res = ene - calc_energy(n_spc, plants)

    return Ecosystem(n_res, n_spc, ene)


def seed(
    system: Ecosystem,
    plants: pd.DataFrame,
    distance: int = 1,
) -> Ecosystem:
    # res, spc, ene = system.resource, system.species, system.energy
    spc, ene = system.species, system.energy
    z, y, x = spc.shape
    seeds = get_neighbors(spc, distance)

    n_spc = spc.copy() + mult_by_layer(seeds, plants.g)
    n_res = ene - calc_energy(n_spc, plants)
    return Ecosystem(n_res, n_spc, ene)


def harvest(
    system: Ecosystem,
    plants: pd.DataFrame,
    n_intervention: int
) -> Ecosystem:
    res, spc, ene = system.resource, system.species, system.energy
    n_spc = spc.copy()
    n_res = np.zeros_like(res)
    human = (1 - 0.3 * np.random.rand())

    # Regularize by resource capacity
    idx = res < 0
    coef = np.ones_like(res)
    coef[idx] = (ene / (-res[idx] + ene))
    n_spc *= human * coef

    # Human Intervention ... harvest(種) + stamping(硬さparams
    # ... 水の利用料/germintion変わる etc...)(セル毎)
    # 収穫の最大化 / 早めにとって再成長を狙うなど / 競合する種を抜く
    # ... 空間的に非対称を入れるか(interaction) / 時間的な非対称性
    rate = spc.sum(1).sum(1)
    rate = (rate / rate.sum()).cumsum()
    spc_inter = [np.argmax(rate > i) for i in np.random.rand(n_intervention)]
    n_spc[spc_inter, :, :] *= human

    # Stamping
    #   z, y, x = spc.shape
    #   rand_pos_x = np.random.randint(0, x, n_intervention)
    #   rand_pos_y = np.random.randint(0, y, n_intervention)
    #   n_spc[:, rand_pos_y, rand_pos_x] *= 0.1

    n_res = ene - calc_energy(n_spc, plants)
    return Ecosystem(n_res, n_spc, ene)


def plant(
    system: Ecosystem,
    plants: pd.DataFrame
):
    pass


def mask(
        system: Ecosystem,
        plants: pd.DataFrame,
        masking: np.ndarray) -> Ecosystem:

    # res, spc, ene = system.resource, system.species, system.energy
    spc, ene = system.species, system.energy

    n_spc = spc.copy()
    n_spc *= masking

    n_res = ene - calc_energy(spc, plants)

    return Ecosystem(n_res, n_spc, ene)


# ---

root = dirname(dirname(__file__))

system, plants = setup(join(root, "data", "landuse.csv"))
res, spc, ene = system.resource, system.species, system.energy

system = Ecosystem(90+res, spc, 100)

buffer = [system]

for i in range(100):
    system = grow(system, plants)
    system = seed(system, plants)
    system = harvest(system, plants, 1)
    buffer.append(system)

result = pd.DataFrame([[b.species.sum(1).sum(1)[i] for b in buffer] for i in range(3)]).T
result.plot().get_figure().savefig(join(root, "out", "city.png"))
