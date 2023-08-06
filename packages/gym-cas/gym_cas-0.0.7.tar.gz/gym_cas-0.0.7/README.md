# GYM CAS

[![PyPI - Version](https://img.shields.io/pypi/v/gym-cas.svg)](https://pypi.org/project/gym-cas)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gym-cas.svg)](https://pypi.org/project/gym-cas)

Hjælpepakke til at bruge Python som CAS (Computational Algebra System) i gymnasiet.

## Installation

```console
pip install gym-cas
```

## Cheatsheet

I nedenstående afsnit antages det at `gym_cas` først importeres således:

```py
from gym_cas import *
```

### B1. Tal- og bogstavregning

```py
expand( udtryk )
factor( udtryk )
```

### B2. Ligninger og uligheder

```py
solve( udtryk )
solve( [udtryk1, udtryk2] )
nsolve( udtryk, start )
```

Bemærk at den nemmeste måde at bruge `solve` i `SymPy` er ved at omforme sin ligning så en af siderne er lig 0. Hvis man fx vil løse ligningen `x/2 = 10` så kan det skrives `solve(x/2-10)`.

### B3. Geometri og trigonometri

```py
Sin( vinkel )
Cos( vinkel )
Tan( vinkel )
aSin( forhold )
aCos( forhold )
aTan( forhold )
```

