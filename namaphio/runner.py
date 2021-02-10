from .simulators import Simulator, Module
from .simulators.example import random_heatmap, CumsumHeatpmap

simulator = Simulator()

userfunc = CumsumHeatpmap()
simulator.setup([
    Module(
        name='Econimpact',
        in_field='all',
        func=userfunc
    ),
    Module(
        name='Ecoimpact',
        in_field='geogrid',
        func=random_heatmap
    )
])
