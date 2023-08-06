from importlib.resources import files
import json
import math
from pathlib import Path
import pickle
from pprint import pprint
import sys

from .core import UnitRegistry
from .parser import ParserError


ureg = UnitRegistry.get_default()
# ureg2 = UnitRegistry.load_default()

# print(ureg1)
# print(ureg2)

# x = pickle.dumps(ureg1)

# print(len(pickle.dumps(ureg1)))
# print(len(pickle.dumps(ureg2)))

# print(x)
# print(pickle.loads(x))
# print(pickle.loads(pickle.dumps(ureg2)))

# ureg = UnitRegistry.load(files("quantops").joinpath("registry.toml").open("rb"))

# x = ureg.meter
# print(x)

# x = 34 * ureg.dimensionless
# print(">", x)

# print(x.format('dimensionless', resolution=(0.1 * ureg.dimensionless)))

# print(ureg.parse_unit('dimensionless'))
# print(ureg.parse_quantity('3'))
x = ureg.parse_quantity('34 l/min')
# x = 34 * ureg.degC

print(x)
print(x.format("flowrate"))
# print(x.format("temperature:kelvin"))

# pprint(ureg._contexts)
# pprint(ureg._assemblies)
# pprint(ureg._units_by_name)

# try:
#   print(ureg.parse('~meter/s**2'))
# except ParserError as e:
#   print(e.message)
#   print(e.area)
#   print(e.area.format())
#   raise


# x = ureg.parse_quantity('10.8 m/s')
# print(x.format('velocity'))

# pprint(ureg.serialize())


# data_path = Path(__file__).parent / "../../javascript/data/registry.json"
# data_path.parent.mkdir(exist_ok=True, parents=True)

# with data_path.open("w") as file:
#   json.dump(ureg.serialize(), file, indent=2)

# json.dump(ureg.serialize(), sys.stdout, indent=None, separators=(',', ':'))


# x = 0.3 * ureg.unit('l') / ureg.unit('min')

# print(x)

# print(x.format('flowrate', 0))


# y = math.inf * ureg.unit('m') ** 3 / ureg.unit('sec')

# print(y)
# print(y.format('flowrate'))


# z = 3.0e-3 * ureg.unit('K')

# print(z)
# print(z.format('physics_temperature', 1e-5))


# x = 3 * ureg.mm
# print(x.format('length', resolution=(10 * ureg.µm)))

# y = 50 * ureg.unit('ug') / ureg.unit('ml')
# print(y.format('dna_concentration', resolution=(0.001 * y)))
