conversions = {
    'n/mm to lb/in': 0.5710147163,
    'n/mm to kgf': 0.1019716213,
    'psi to bar': 0.0689476,
}

def newtonsToKgf(value: float):
    return value * conversions["n/mm to kgf"]

def newtonsToLbs(value: float):
    return value * conversions["n/mm to lb/in"]

def kgfToNewtons(value:float):
    return value / conversions["n/mm to kgf"]

def lbsToNewtons(value: float):
    return value / conversions["n/mm to lb/in"]

def convertNewtons(value: float):
    return '{:.2f} lb/in, {:.2f} kgf'.format(newtonsToLbs(value), newtonsToKgf(value))

def convertPoundsPerInch(value: float):
    newtons = lbsToNewtons(value)
    return '{:.2f} n/mm, {:.2f} kgf'.format(newtons, newtonsToKgf(newtons))

def convertKgf(value: float):
    newtons = kgfToNewtons(value)
    return '{:.2f} n/mm, {:.2f} lb/in'.format(newtons, newtonsToLbs(newtons))

def psiToBar(value: float):
    return value * conversions["psi to bar"]

def barToPsi(value: float):
    return value / conversions["psi to bar"]

def convertPsi(value: float):
    return '{:.2f} bar'.format(psiToBar(value))

def convertBar(value: float):
    return '{:.2f} psi'.format(barToPsi(value))

def convertCm(value: float):
    return '{:.1f} in'.format(value * 0.393701)

def convertInch(value: float):
    return '{:.1f} cm'.format(value / 0.393701)

convertMap = {
    'lb/in': convertPoundsPerInch,
    'lbin': convertPoundsPerInch,
    'n/mm': convertNewtons,
    'kgf': convertKgf,
    'kgf/mm': convertKgf,
    'psi': convertPsi,
    'bar': convertBar,
    'cm': convertCm,
    'in': convertInch,
}

def convert(unit: str, value: float):
    normalizedUnit = unit.lower()
    if normalizedUnit in convertMap:
        return convertMap[normalizedUnit](value)

    raise NameError('unit')
