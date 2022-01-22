convertMap = {
    'lb/in': 'lb/in',
    'lbin': 'lbin',
    'n/mm': 'n/mm',
    'kgf': 'kgf',
    'kgf/mm': 'kgf/mm',
    'psi': 'psi',
    'bar': 'bar',
    'cm': 'cm',
    'in': 'in',
}

if 'lb/in' in convertMap:
    print(convertMap['lb/in'])

if 'notfound' in convertMap:
    print(convertMap['notfound'])
else:
    print('notfound was not found')
