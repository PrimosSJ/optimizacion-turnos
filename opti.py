import pulp
from math import floor, ceil
from collections.abc import Iterable

def parse_schedule(schedule, no_blocks):
    parsed_schedule = ''
    for i, day in enumerate('lmxjv'):
        blocks = []
        for block, availability in enumerate(schedule[i*no_blocks: i*no_blocks+no_blocks]):
            if availability:
                blocks.append(str(block))
        if len(blocks):
            parsed_schedule += f'{day}{",".join(blocks)}'
    return parsed_schedule

def get_schedule(primos: Iterable, no_blocks: int, primos_per_shift: int = 2):
    # Posibles errores
    if not (0 < no_blocks <= 8):
        raise ValueError('La jornada diruna abarca desde el 1-2 hasta el 15-16 (8 turnos)')
    if not len(primos):
        raise ValueError('<primos> está vacío')
    if primos_per_shift > len(primos):
        raise ValueError('Se requieren más primos por turno que los primos que existen')
    
    # Algunas variables que necesitaremos después...
    days = 'lmxjv'
    shifts = range(len(days)*no_blocks)
    no_shifts_per_primo = len(days)*no_blocks*primos_per_shift/len(primos)
    satisfaction = [pulp.LpVariable(name=f'satisfaction_{shift}', lowBound=0, cat=pulp.LpInteger) for shift in shifts]
    primo_has_shift, primo_shift_weight = {}, {}
    for primo in primos:
        # Por cada primo y por cada turno ponemos una variable binaria que indica si el primo tiene (o no) ese turno.
        primo_has_shift[primo] = [pulp.LpVariable(name=f'has_shift_{primo.rol}_{shift}', cat=pulp.LpBinary) for shift in shifts]
        # Establecemos el peso de cada turno para cada primo (0 si no puede, 1 si puede, 2 si puede y lo quiere)
        primo_shift_weight[primo] = []
        for day, _ in enumerate(days):
            for block in range(no_blocks):
                # OJO: En la BD, los horarios tienen 40 turnos, es decir que cada día tiene 8 bloques, por eso <shift := day*8 + block>
                
                #primo_shift_weight[primo].append((primo.desire_schedule[shift := day*8 + block] + 1)*(not primo.bussy_schedule[shift]))
                shift = day * 8 + block
                primo_shift_weight[primo].append((primo.desire_schedule[shift] + 1) * (not primo.bussy_schedule[shift]))


    # Definimos el modelo para que maximice la satisfacción por bloque
    model = pulp.LpProblem(sense=pulp.LpMaximize)
    model += sum(satisfaction)
    
    # Restricciones por turno
    for shift in shifts:
        # Tienen que haber <primos_per_shift> primos por turno.
        pps_constraint = sum(primo_has_shift[primo][shift] for primo in primos)
        model += pulp.LpConstraint(e=pps_constraint, sense=pulp.LpConstraintEQ, rhs=primos_per_shift, name=f'primos_per_shift_{shift}')
        
        # No te puede tocar un turno donde tienes clases
        maxsat_constraint = satisfaction[shift] - sum(primo_has_shift[primo][shift] * primo_shift_weight[primo][shift] for primo in primos)
        model += pulp.LpConstraint(e=maxsat_constraint, sense=pulp.LpConstraintEQ, rhs=0)

    # Restricciones por primo
    for primo in primos:
        # Cada primo debe tener <no_shifts_per_primo> turnos
        no_shifts = pulp.LpVariable(name=f'no_shifts_{primo.rol}', lowBound=floor(no_shifts_per_primo), upBound=ceil(no_shifts_per_primo), cat=pulp.LpInteger)
        nt_constraint = no_shifts - sum(primo_has_shift[primo])
        model += pulp.LpConstraint(e=nt_constraint, sense=pulp.LpConstraintEQ, rhs=0, name=f'no_shifts_constraint_{primo.rol}')
    
    # Esta restricción evita que algún primo salga muy perjudicado
    mean = sum(satisfaction)/len(satisfaction)
    std = sum(var - mean for var in satisfaction)/len(satisfaction)
    model += std <= 2*primos_per_shift/len(satisfaction)

    # Resolvemos
    model.solve()
    schedule, variables = {}, {var.name: var.value() for var in model.variables()}
    for primo in primos:
        schedule[primo] = parse_schedule([bool(variables[f'has_shift_{primo.rol}_{shift}']) for shift in shifts], no_blocks)
    return schedule

if __name__ == '__main__':
    from primos import primos
    result = get_schedule(primos, 7)
    for primo in primos:
        print(primo.rol, result[primo])
    with open('primos.csv', 'w', encoding='utf-8') as file:
        for primo in primos:
            file.write(f'{primo.rol};{primo.mail};{primo.name};{primo.nick};{result[primo]}\n')
