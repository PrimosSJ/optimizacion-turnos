import pulp
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


def get_schedule(primos: Iterable, new_primos: Iterable, primos_per_shift: Iterable, shifts_per_primo: int):
    if not len(primos):
        raise ValueError('<primos> está vacío')

    no_blocks = len(primos_per_shift[0])

    # Algunas variables que necesitaremos después...
    days = 'lmxjv'
    shifts = range(len(days)*no_blocks)
    total_shifts = sum(sum(req if req > 0 else 0 for req in day) for day in primos_per_shift)
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

                # primo_shift_weight[primo].append((primo.desire_schedule[shift := day*8 + block] + 1)*(not primo.bussy_schedule[shift]))
                shift = day * 8 + block
                primo_shift_weight[primo].append((primo.desire_schedule[shift] + 1) * (not primo.bussy_schedule[shift]))

    # Definimos el modelo para que maximice la satisfacción por bloque
    model = pulp.LpProblem(sense=pulp.LpMaximize)
    model += sum(satisfaction)
    # Restricciones por turno
    for shift in shifts:
        block = shift % no_blocks
        day = int(shift / no_blocks)

        primos_in_block = primos_per_shift[day][block]
        pps_constraint = sum(primo_has_shift[primo][shift] for primo in primos)

        # Si primos_in_block es negativo, no se puede asignar ese turno
        if (primos_in_block < 0):
            model += pulp.LpConstraint(e=pps_constraint, sense=pulp.LpConstraintEQ, rhs=0, name=f'primos_per_shift_{shift}')
            continue

        # Tienen que haber por lo menos <primos_per_shift> primos por turno, y como máximo 2.
        model += pulp.LpConstraint(e=pps_constraint, sense=pulp.LpConstraintGE, rhs=primos_in_block if primos_in_block != 0 else 1, name=f'primos_per_shift_{shift}')
        model += pulp.LpConstraint(e=pps_constraint, sense=pulp.LpConstraintLE, rhs=2 if block != 7 else 1, name=f'primos_per_shift_limit_{shift}')

        # No te puede tocar un turno donde tienes clases
        maxsat_constraint = satisfaction[shift] - sum(primo_has_shift[primo][shift] * primo_shift_weight[primo][shift] for primo in primos)
        model += pulp.LpConstraint(e=maxsat_constraint, sense=pulp.LpConstraintEQ, rhs=0)

        # No pueden haber primos nuevos solos, y tampoco puede haber más de uno en turno normal
        np_constraint = sum(primo_has_shift[primo][shift] for primo in new_primos)

        if (primos_in_block == 1):
            model += pulp.LpConstraint(e=np_constraint, sense=pulp.LpConstraintEQ, rhs=0, name=f'no_new_primos_{shift}')
        elif (primos_in_block != 0):
            model += pulp.LpConstraint(e=np_constraint, sense=pulp.LpConstraintLE, rhs=1, name=f'new_primos_in_shift_{shift}')

    # Restricciones por primo
    for primo in primos:
        # Cada primo debe tener <no_shifts_per_primo> turnos
        nt_constraint = sum(primo_has_shift[primo])
        model += pulp.LpConstraint(e=nt_constraint, sense=pulp.LpConstraintEQ, rhs=shifts_per_primo, name=f'no_shifts_constraint_{primo.rol}')

    # Esta restricción evita que algún primo salga muy perjudicado
    mean = sum(satisfaction)/len(satisfaction)
    std = sum(var - mean for var in satisfaction)/len(satisfaction)
    model += std <= 2*(total_shifts / len(primos_per_shift))/len(satisfaction)

    # Resolvemos
    model.solve()
    schedule, variables = {}, {var.name: var.value() for var in model.variables()}
    for primo in primos:
        schedule[primo] = parse_schedule([bool(variables[f'has_shift_{primo.rol}_{shift}']) for shift in shifts], no_blocks)
    return schedule


if __name__ == '__main__':
    from primos import primos, new_primos

    req = [
            #                 A
            # 0   1   2   3   4   5   6   7
            [-1,  0,  0,  0,  1,  0,  0,  1],  # L
            [+1,  0,  0,  0,  1,  0,  0,  1],  # M
            [-1,  0,  0,  0,  0,  2,  1,  1],  # X
            [-1,  0,  0,  0,  0,  2,  1,  1],  # J
            [-1,  2,  2,  2,  2,  1,  1,  1],  # V
            ]

    shifts_per_primo = 3  # Daniel los calcula manualmente
    result = get_schedule(primos, new_primos, req, shifts_per_primo)

    for primo in primos:
        print(primo.nick, result[primo])
    with open('primos.csv', 'w', encoding='utf-8') as file:
        for primo in primos:
            file.write(f'{primo.rol};{primo.mail};{primo.name};{primo.nick};{result[primo]}\n')
