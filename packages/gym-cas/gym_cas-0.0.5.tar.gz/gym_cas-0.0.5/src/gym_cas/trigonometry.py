from sympy import cos, sin, tan, acos, asin, atan, pi, N

def Sin(v: float):
    '''
    Hjælpefunktion til at udregne sinus til vinklen i grader.

    Brug sin fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(sin(v / 180 * pi))

def Cos(v: float):
    '''
    Hjælpefunktion til at udregne cosinus til vinklen i grader.

    Brug cos fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(cos(v / 180 * pi))


def Tan(v: float):
    '''
    Hjælpefunktion til at udregne tangens til vinklen i grader.

    Brug tan fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(tan(v / 180 * pi))

def aSin(val: float):
    '''
    Hjælpefunktion til at udregne invers sinus til sinusværdien.

    Brug asin fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(asin(val) / pi * 180)

def aCos(val: float):
    '''
    Hjælpefunktion til at udregne invers cosinus til cosinusværdien.

    Brug acos fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(acos(val) / pi * 180)


def aTan(val: float):
    '''
    Hjælpefunktion til at udregne invers tangens til tangensværdien.

    Brug atan fra sympy hvis der skal arbejdes med udtrykket (fx differentieres).
    '''
    return N(atan(val) / pi * 180)

if __name__ == "__main__":
    print(Sin(90))
    print(Sin(135))
    print(Sin(180))
    print(Cos(90))
    print(Cos(135))
    print(Cos(180))
    print(Tan(90))
    print(Tan(135))
    print(Tan(180))
    print(aSin(1))
    print(aSin(0.5))
    print(aSin(-1))
    print(aCos(1))
    print(aCos(0.5))
    print(aCos(-1))
    print(aTan(2))
    print(aTan(1))
    print(aTan(-0.5))
