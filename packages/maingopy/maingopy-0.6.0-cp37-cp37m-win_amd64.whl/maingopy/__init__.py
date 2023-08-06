'''A Python package for using MAiNGO - McCormick-based Algorithm for mixed-integer Nonlinear Global Optimization

MAiNGO is a deterministic global optimization solver for mixed-integer nonlinear programming problems.
For information about the capabilities and use of MAiNGO, please refer to the documentation at https://avt-svt.pages.rwth-aachen.de/public/maingo/.
This version of maingopy also contains the extension module melonpy, which enables the use of MeLOn (https://git.rwth-aachen.de/avt.svt/public/melon),
a toolbox containing machine learning models for use in optimization problems to be solved by MAiNGO.
'''
from ._maingopy import *
from . import melonpy