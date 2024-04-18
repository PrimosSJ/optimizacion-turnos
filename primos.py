from re import findall

class Primo:
    def __init__(self, rol, mail, name, nick, bussy, desire):
        self.rol = rol
        self.mail = mail
        self.name = name
        self.nick = nick
        self.bussy_schedule = bussy
        self.desire_schedule = desire

_schedules = [
    ('2018731129','felipe.rojass@sansano.usm.cl','Felipe Andrés Rojas Saavedra','Puyon',"l2,5,6m2,4x0,1,2,3,4,5,6,7j1,2,5v0,1,2,3,4,5,6,7","l1,3,4m0,1,3,5j0,3,4"),
    ('2020736162','gabriel.vergaraa@usm.cl','Gabriel Vergara Alonso' ,'Gabotel',"l0,2,4,5,7m0,2,4,7x2,5,7j1,2,4,7v0,1,2,3,4,5,6,7","l3x3,4j3,5"),
    ('2020115753','francisco.gonzalezgu@usm.cl','Francisco Gonzalez Guerra (alumno)','Pancho',"l4,5m4,5x2,4,5,6j4v0,1,2,3,4,5,6","l3,6m3,6x3j3,5,6"),
    ('2021045864','Bastian.Navarrete@usm.cl','Cristóbal Tirado Morales','Turbo',"l0,1,2,3,4,5,6,7m0,1,2,3,4,5,6,7x0,1,2,6,7j0,1,2,3,4,5,6,7v0,1,2,4,5,6,7","x3,4,5v3"),
    ('2020735557','Felipe.Guicharrousse@usm.cl','Felipe Guicharrousse Rojas (alumno)','Pipeño',"l0,1,2,5m0,1,2,4x0,1,2,5,6j0,1,2,4,5v0,1","l3,4m3x3,4j3"),
    ('2020735107','Cristobal.Tirado@usm.cl','Bastián Navarrete Camus','Chrona',"l0,1,2,5,6,7m0,1,2,3,4,5,6,7x0,1,6,7j0,1,2,3,4,5,6,7v0,1,2,5,6,7","l3,4x2,3,4,5v3,4"),
    ('2021735828','diego.duarte@usm.cl','Diego Duarte Madrid','diegod',"l3,6m0,1,4,6x3,4j0,1,2,3,4,5,6v0,2,3,6","l2,5m2,5x1,2,5v5"),
    ('2020045798','rodrigo.ramirezca@usm.cl','Rodrigo Ramirez Catrileo','Zurickata',"l1,2,3,4,5,7m2,4,5,7x2,3,4,5,6,7j1,4,5,7v0,1,2,3,4,5,6,7","m3,6x0,1j2,3,6"),
    ('2020735743','Carlos.Kuhn@usm.cl','Carlos Kuhn','Kuhn',"l2m2,4,5,6x2,4,5,6j1,2,4,5v4,5","l0,1,3,4m0,1,3x0,1,3j0,3"),
    ('2023735574','pvergara@usm.cl','Paula Francisca Vergara Cooper','Paula Vergara',"l0,3,5m2,5,6x0,3,5j2,4,5v0,3,6","l2,4m3,4x2,4j3v1,2,4,5"),
    ('2018235245','vicente.mackenzie@sansano.usm.cl','Vicente Gustavo Mackenzie Maturana','Makenki',"l2,3,5,6m5x4,5j0,2,6","l4j1,3,4,5"),
    ('2021046640','diego.debarca@usm.cl','Diego Debarca Pulgar (alumno)','Champi',"l1,2,3,4,5m2,4x2,5j2,4,5,6,7v0,1,2,3,4,5,6,7","m1,3,5x1,3,4j1,3"),
    ('2020046204','Yasmine.perez@usm.cl','Yasmine Perez Cerda (alumno)','Mimii',"l0,2,3,4,5,6m1,2,4x0,2,3,5,6j1,2,5v0,1,2,3,4,5","l1m0x1j0,4"),
    ('2020735522','maximiliano.tapiac@usm.cl','Maximiliano Tapia Castillo (alumno)','Choche',"l2,3,5,6m2,4x2,3j1,2,4,5,6v4","l1m1x1v1,2"),
    ('2018235458','carlos.mundaca@sansano.usm.cl','Carlos Gabriel Mundaca Fernández','Carlos',"l1,2,4,5,6,7m0,1,2x1,2j1,2,5,6,7v3,4,5","m3,4,5x0j0v0,1,2"),
    ('2021046500','sofia.rios@usm.cl','Sofia Rios Nuñez (alumno)','Sofi',"l0,1,2,3,4,5,6,7m0,2,5,6,7x0,2,5,6,7j0,1,2,3,4,5,6,7v0,1,2,3,4,5,6,7","m1,3,4x1,3,4")
]


def _parse(schedule):
    days = 'lmxjv'
    parsed_schedule = [False]*40
    for day in findall(r'([lmxjv](?:\d,)*\d)', schedule):
        for block in day[1:].split(','):
            parsed_schedule[8*days.index(day[0]) + int(block)] = True
    return parsed_schedule

primos = []
for rol, mail, name, nick, bussy, desire in _schedules:
    bussy, desire = _parse(bussy), _parse(desire)
    primos.append(Primo(rol, mail, name, nick, bussy, desire))
