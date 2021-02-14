import numpy as np
import pandas as pd

from .types import Ecosystem
from .utils import mult_by_layer
from .operations import calc_energy

def grow(
  system: Ecosystem, 
  plants: pd.DataFrame
) -> Ecosystem:
  
  res, spc, ene = system.resource, system.species, system.energy
  
  n_spc = np.zeros_like(spc)
  n_res = np.zeros_like(res)
  
  N = spc
  K_ene = res + mult_by_layer(N, plants.e)
  K_num = mult_by_layer(K_ene, 1/plants.e)
  K_num[K_num.round(4) == 0] = 1e-4

  # Ligustic
  n_spc = N + mult_by_layer(N * (1 - N / K_num), plants.r)
  n_res = ene - calc_energy(n_spc, plants)
  
  return Ecosystem(n_res, n_spc, ene)