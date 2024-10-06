import json
import math

skel_alpha = None
with open('skeleton_alphabet.json') as skel_alpha_f:
  skel_alpha = json.load(skel_alpha_f)

# dimensions of the base
base_dim = {
  's' : 1.,                            # base square
  'rw': math.sqrt(2.) / 2.,            # base rectangle
  'l' : 4. / (3. * math.sqrt(2.) + 2.) # base square for lowercase characters
}

# diameters of the circles used for constructing characters
circ_dia = {
  'c': 1.,             # base circle
  't': 0.4716,         # top circle for uppercase characters
  'b': 0.5284,         # bottom circle for uppercase characters
  'u': base_dim['rw'], # circle for construction a capital U and S
  'k': base_dim['l'],  # base circle for lowercase characters
  'p': base_dim['l'] * math.sqrt(2.) / 2,
  'h': base_dim['l'] / 2.
}

# dimensions of the horizontal line of a capital A
A_dim = {
  'ax': 0.3820 * base_dim['rw'] / 2.,
  'ay': 0.3820,
  'al': (1. - 0.3820) * base_dim['rw']
}

# generate all other revelant circle dimensions
upper_circ = {key: dim for char, val in circ_dia.items() for key, dim in {
  f"{char}r":  val / 2.,                              # radius
  f"{char}d": (val / 2.) * math.sqrt(2.) / 2.,        # coord of diagonal point
  f"{char}c": (val / 2.) * (math.sqrt(2.) - 1.),      # distance to control point of quadratic curve
  f"{char}m": (val / 2.) * (1. - math.sqrt(2.) / 2.), # radius minus coord of diagonal point
  f"{char}p": (val / 2.) * (1. + math.sqrt(2.) / 2.)  # radius plus coord of diagonal point
}.items()}

dimensions = base_dim | circ_dia | upper_circ | A_dim

svg_size       = (36, 6)
svg_attributes = {
  'style': "fill:none;stroke:black;stroke-width:0.1;stroke-linecap:round;stroke-linejoin:round"
}

with open('skeleton_alphabet.svg', 'w') as svg:
  svg.write(f"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")

  svg_attr = ' '.join(f"{key}=\"{val}\"" for key, val in svg_attributes.items())
  svg.write(f"<svg width=\"{svg_size[0]}mm\" height=\"{svg_size[1]}mm\" viewBox=\"0 0 {svg_size[0]} {svg_size[1]}\" xmlns=\"http://www.w3.org/2000/svg\" {svg_attr}>\n")

  xpos = .5
  for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    svg.write(f"  <path transform=\"translate({xpos},1.5)\" d=\"{skel_alpha[char]['d'].format(**dimensions)}\" />\n")
    xpos += eval(skel_alpha[char]['w'].format(**dimensions)) + .25

  xpos = .5
  for char in 'abcdefghijklmnopqrstuvwxyz':
    svg.write(f"  <path transform=\"translate({xpos},3.5)\" d=\"{skel_alpha[char]['d'].format(**dimensions)}\" />\n")
    xpos += eval(skel_alpha[char]['w'].format(**dimensions)) + .25

  xpos = .5
  for char in '0123456789':
    svg.write(f"  <path transform=\"translate({xpos},5.5)\" d=\"{skel_alpha[char]['d'].format(**dimensions)}\" />\n")
    xpos += eval(skel_alpha[char]['w'].format(**dimensions)) + .25

  svg.write("</svg>\n")
