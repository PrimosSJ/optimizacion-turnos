from re import findall
import csv


class Primo:
    def __init__(self, rol, mail, name, nick, bussy, desire):
        self.rol = rol
        self.rol_safe = rol[:-2] + '_' + rol[-1]
        self.mail = mail
        self.name = name
        self.nick = nick
        self.bussy_schedule = bussy
        self.desire_schedule = desire

    def __str__(self):
        return self.rol_safe

    def __hash__(self):
        return hash(self.rol_safe)

    def __eq__(self, other):
        if isinstance(other, Primo):
            return other.rol_safe == self.rol_safe
        return False


def datos_a_tupla(filename):
    data_list = []

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)

        for row in reader:
            data_tuple = tuple(row)
            data_list.append(data_tuple)

    return data_list


_schedules = datos_a_tupla('input.csv')


def _parse(schedule):
    days = 'lmxjv'
    parsed_schedule = [False]*45
    for day in findall(r'([lmxjv](?:\d,)*\d)', schedule):
        for block in day[1:].split(','):
            parsed_schedule[8*days.index(day[0]) + int(block)] = True
    return parsed_schedule


primos = []
new_primos = []

for rol, mail, name, nick, bussy, desire, new in _schedules:
    bussy, desire = _parse(bussy), _parse(desire)
    primo = Primo(rol, mail, name, nick, bussy, desire)
    primos.append(primo)

    if (new == 'True' or new == 'true'):  # Ooops
        new_primos.append(primo)
