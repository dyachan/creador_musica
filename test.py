#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Secuencia import Secuencia
from mingus.containers.Note import Note

s = Secuencia(4, 4, 40, Note('C', 4), Secuencia.ESCALA[0])
s.magiarSecuencia(1, 20, 70, 30, 20, 30)
s.mostrar()
print("")
s.tocar()
