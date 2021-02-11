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


def random_ecosystem(
  field_shape: Tuple[int, int],
  num_species: int,
  base_resource: int = 0
):
  res = np.zeros(field_shape) + base_resource
  spc = np.zeros((num_species, *field_shape))
  return Ecosystem(res, spc)


