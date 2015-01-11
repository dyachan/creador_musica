#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Secuencia import Secuencia
from mingus.containers.Note import Note

s = Secuencia(4, 4, 2, Note('C', 4), Secuencia.ESCALA[0])
s.magiarSecuencia(1, 20, 60, 30, 20, 30)

s2 = Secuencia(4, 4, 2, Note('D', 4), Secuencia.ESCALA[4])
s2.magiarSecuencia(5, 0, 20, 100, 60, 10)

s.mostrar().tocar()
s.cambiarTono(Note('A', 3)).mostrar().tocar()
s2.mostrar().tocar()
s2.invertir().mostrar().tocar()



'''
s.mostrar()
print("")
s.tocar()

inv = s.copiar()
inv.invertir()
s2.mostrar()
print("")
s2.tocar()

s.mostrar()
print("")
s.tocar()
'''