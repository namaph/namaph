import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from typing import NamedTuple, Tuple

class Ecosystem(NamedTuple):
  resource: np.ndarray
  species: np.ndarray
  energy: float = 10
  
  def describe(self):
    res = self.resource.reshape(-1)
    spc = self.species.reshape(self.species.shape[0], -1)    
    df = pd.DataFrame({"res": res, **{f"spc_{i}": s for i, s in enumerate(spc)}})
    return df.describe()
  
  def heatmap(self, annot=True):
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    z, y, x = self.species.shape
    sns.heatmap(self.resource, ax=ax[0], annot=annot)
    ax[0].set_title('Resource')
    sns.heatmap(np.dstack([np.zeros((y,x)), *self.species]).argmax(axis=2), ax=ax[1], annot=annot)
    ax[1].set_title('Species')
    
  
  def round(self, r:int = 2):
    res, spc = self.resource, self.species
    return Ecosystem(res.round(r), spc.round(r))
    
  
  def __repr__(self):
    return f"""Ecosystem(
resource: \n{self.resource}
species: \n{self.species}
)"""