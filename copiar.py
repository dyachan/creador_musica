#! /usr/bin/env python2
# -*- coding: utf-8 -*-

from mingus.containers.Note import Note

def nota(nota):
	return Note(nota.name, nota.octave)
