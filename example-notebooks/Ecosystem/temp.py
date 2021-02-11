import numpy as np
import pandas as pd

from typing import Tuple

from .types import Ecosystem
from .operations import calc_energy
from .utils import default_ecosystem


def setup(plants_path: str) -> Ecosystem:
  system = default_ecosystem((5, 5), 3, 10)
  plants = pd.read_csv(plants_path, index_col=0)
  res, spc = system.resource, system.species

  spc[0, 0, 0] = 50
  spc[1, 4, 4] = 10
  spc[[2,2], [0, 4], [4, 0]] = 5

  energy = calc_energy(spc, plants)
  res -= energy

  system = Ecosystem(res, spc)
  return system, plants