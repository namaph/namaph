import numpy as np
import pandas as pd

from typing import Tuple

from .types import Ecosystem

def mult_by_layer(tensor: np.ndarray, vector: np.ndarray):
  params = np.array([np.eye(tensor.shape[2]) * v for v in vector])
  return tensor @ params

def default_ecosystem(
  field_shape: Tuple[int, int],
  num_species: int,
  base_resource: int = 0
):
  res = np.zeros(field_shape) + base_resource
  spc = np.zeros((num_species, *field_shape))
  return Ecosystem(res, spc, base_resource)

def set_random(field: np.ndarray, cpf: int, ran=[10,50], spec:int = 100) -> np.ndarray:
  spec, col, row = field.shape
  temp = field
  for _ in range(cpf):
    init_pos = np.hstack((
      np.arange(spec)[:, None],
      np.random.randint(0, col, (spec, 1)),
      np.random.randint(0, row, (spec, 1))
    ))
    init_val = np.random.randint(ran[0], ran[1], (spec))
    temp[tuple(map(tuple, init_pos.T))] += init_val
  return temp