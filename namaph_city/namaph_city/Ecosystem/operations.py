import numpy as np
import pandas as pd

from .utils import mult_by_layer

def calc_energy(spc: np.ndarray, plants: pd.DataFrame) -> np.ndarray:
  energy = mult_by_layer(spc, plants.e)
  return energy.sum(axis=0)

def get_neighbors(
  field: pd.DataFrame,
  distance: int
) -> pd.DataFrame:
  z, y, x = field.shape
  
  d = distance
  s = 2*d
  
  f = np.zeros((z, y+2*d, x+2*d))
  f[:, d:-d, d:-d] = field
  
  top  = f[:, :-s,d:-d]
  btm  = f[:,s:  ,d:-d]
  lt   = f[:,d:-d, :-s]
  rt   = f[:,d:-d,s:  ]

  ltop = f[:, :-s, :-s]
  lbtm = f[:,s:  , :-s]
  rtop = f[:, :-s,s:  ]
  rbtm = f[:,s:  ,s:  ]
  
  return top + btm + lt + rt + ltop + lbtm + rtop + rbtm