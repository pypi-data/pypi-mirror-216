import math
from pyproj import Proj, transform

class Translator:

  def __init__(self):
    self.degree_proj = Proj(init='EPSG:4326')
    self.mercator_proj = Proj(init='EPSG:3857')

  def slippy2degree(self, x, y, z):
    n = 1 << z
    long_degrees = x / n * 360.0 - 180.0
    lat_radians = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_degrees = math.degrees(lat_radians)
    return lat_degrees, long_degrees

  def slippy2bbox(self, x, y, z):
    top_degrees, left_degrees = self.slippy2degree(x, y+1, z)
    bottom_degrees, right_degrees = self.slippy2degree(x+1, y, z)
    left, top = transform(self.degree_proj, self.mercator_proj, left_degrees, top_degrees)
    right, bottom = transform(self.degree_proj, self.mercator_proj, right_degrees, bottom_degrees)
    return left, top, right, bottom

  def translate(self, x, y, z, template):
    left, top, right, bottom = self.slippy2bbox(x, y, z)
    bbox = f'{left},{top},{right},{bottom}'
    return template.replace("{bbox}", bbox)
