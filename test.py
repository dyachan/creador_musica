#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from Secuencia import Secuencia
from mingus.containers.Note import Note

s = Secuencia(4, 4, 2, Note('C', 4), Secuencia.ESCALA[0])
s.magiarSecuencia(1, 100, 100, 0, 0)