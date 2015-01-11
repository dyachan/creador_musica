#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Secuencia import Secuencia
from mingus.containers.Note import Note

s = Secuencia(4, 4, 12, Note('C', 4), Secuencia.ESCALA[0])
s.magiarSecuencia(1, 20, 70, 0, 0, 10)
s.mostrar()
print("")
s.tocar()
