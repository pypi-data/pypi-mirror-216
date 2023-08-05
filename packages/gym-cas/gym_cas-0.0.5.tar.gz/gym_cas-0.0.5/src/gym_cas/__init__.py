# SPDX-FileCopyrightText: 2023-present JACS <jacs@zbc.dk>
#
# SPDX-License-Identifier: MIT

from .trigonometry import Sin,Cos,Tan,aSin,aCos,aTan
from sympy import *
from sympy.abc import *

if __name__ == "__main__":
    Sin(x)
    Cos(y)
    Tan(z)
    aSin(x)
    aCos(y)
    aTan(z)