from .simulators import Simulator, Module
from .simulators.example import random_heatmap, CumsumHeatpmap

simulator = Simulator()

simulator.setup([
    Module(
        name='Econimpact',
        in_field='geogrid',
        func=random_heatmap
    ),
    Module(
        name='Ecoimpact',
        in_field='geogrid',
        func=CumsumHeatpmap()
    )
])
