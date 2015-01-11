#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import random
import sys

from mingus.containers.Bar import Bar
from mingus.containers.Note import Note
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.Track import Track

import mingus.core.notes as _notes
import mingus.core.scales as _scales

from mingus.midi import fluidsynth

import copiar

# agregar sonidos
fluidsynth.init("Gort's_MiniPiano_J1.SF2", "alsa")

class Secuencia:
	""" clase que controla una secuencia de notas.
	"""

	ESCALA = [
		_scales.ionian,
		_scales.dorian,
		_scales.phrygian,
		_scales.lydian,
		_scales.mixolydian,
		_scales.aeolian,
		_scales.locrian
	]

	def __init__(self, pulso, tiempo, compases, tono, modo):
		""" creación del track con silencios
		"""

		self.pulso = pulso
		self.tiempo = tiempo
		self.compases = compases
		self.tono = tono
		self.modo = modo

		self.track = Track()
		buffBar = Bar(self.tono, meter=(self.tiempo, self.pulso))
		for _ in range(compases*tiempo):
			self.track.add_notes(None, pulso)


	def obtenerNota(self, compas, tiempo):
		"""	obtener un arreglo de notas que representan en el mismo orden las notas de las posiciones solicitadas
		"""

		return self.track[compas][tiempo]

	def cambiarNota(self, compas, tiempo, nota):
		""" cambia la nota posicionada en un compás y tiempo determinado por una nota deseada
		"""

		self.track[compas][tiempo][2] = NoteContainer(nota)

	def agregarTrack(self, track):
		""" agrega el track dado al de la secuencia 
		"""

		raise NameError('NoImplementadoTodavia')

	def cortarInicio(self, compases):
		""" elimina la cantidad de compases elegidos del inicio de la secuencia
		"""

		raise NameError('NoImplementadoTodavia')

	def cortarfinal(self, compases):
		""" elimina la cantidad de compases elegidos del final de la secuencia
		"""

		raise NameError('NoImplementadoTodavia')

	def invertir(self):
		""" invierte la secuencia
		"""

		nt = Track()
		for c in range(self.compases-1, -1, -1):
			for t in range(self.tiempo-1, -1, -1):
				nt.add_notes(self.obtenerNota(c, t)[2], self.pulso)
		self.track = nt
		return self

	def cambiarTono(self, tono):
		""" cambia la tonal de la secuencia
		"""

		tonoViejo = Note(self.tono.name, self.tono.octave)
		self.tono = tono

		intervalo = int(tono) - int(tonoViejo)
		funcion = "augment"
		if int(tonoViejo) > int(tono):
			intervalo *= -1
			funcion = "diminish"

		for compas in self.track[:]:
			for notas in compas[:]:
				if notas[2]:
					for nota in notas[2][:]:
						for _ in range(intervalo):
							getattr(nota, funcion)()
						# TODO hacer que se saquen los accidentes rebundantes
						getattr(nota, "remove_redundant_accidentals")()
		return self

	def cambiarModo(self, modo):
		""" cambia el modo de la secuencia
		"""

		notas_de_modo = self.modo(self.tono.name)
		self.modo = modo

		for compas in self.track[:]:
			for notas in compas[:]:
				if notas[2]:
					for nota in notas[2][:]:
						nota.name = self.modo(self.tono.name)[notas_de_modo[:].index(nota.name)]
		return self

	def magiarSecuencia(self, nota, pSubIni, pSubFin, pBajIni, pBajFin, pMod=0, intervalos=[1, 2, 3, 4, 5, 6, 7], octava=4):
		""" crea una secuencia partiendo de una nota; subiendo, bajando o manteniendo la tonalidad con un cierto porcentaje al inicio y al final cambiando de forma gradual; con cierta probabilidad de modificar la nota por sobreescribirla; para un conjunto de intervalos permitidas
		"""

		if pSubIni < 0 or pSubFin < 0 or pBajIni < 0 or pBajFin < 0 or pMod < 0:
			raise NameError('ProbabilidadNegativa')

		if pSubIni > 100 or pSubFin > 100 or pBajIni > 100 or pBajFin > 100 or pMod > 100:
			raise NameError('ProbabilidadSobre100')

		if pSubIni+pBajIni > 100 or pSubFin+pBajFin > 100:
			raise NameError('SumaProbabilidadSobre100')

		if nota not in intervalos:
			raise NameError('NotaNoHabilitada')

		pSubIni /= 100.0
		pSubFin /= 100.0
		pBajIni /= 100.0
		pBajFin /= 100.0
		pMod /= 100.0

		cambioSub = (pSubFin-pSubIni)/(self.compases*self.tiempo)
		cambioBaj = (pBajFin-pBajIni)/(self.compases*self.tiempo)

		grado_actual = nota
		nota_actual = Note(self.modo(self.tono.name)[grado_actual-1], octava)
		for c in range(self.compases):
			for t in range(self.tiempo):
				# agregar la primera nota a la secuencia
				if c == t == 0:
					self.cambiarNota(c, t, copiar.nota(nota_actual))
					continue
				
				# ver si la tonalidad sube, baja o se mantiene
				r = random.random()
				mod = 0
				if r < pSubIni:
					# sube
					mod = 1

					sig_grado = intervalos[(intervalos.index(grado_actual)+1)%len(intervalos)]
					nota_actual = Note(self.modo(self.tono.name)[sig_grado-1], nota_actual.octave)
					if grado_actual == intervalos[len(intervalos)-1]:
						nota_actual.octave_up()

				elif r > 1 - pBajIni:
					# baja
					mod = -1

					sig_grado = intervalos[(intervalos.index(grado_actual)-1)%len(intervalos)]
					nota_actual = Note(self.modo(self.tono.name)[sig_grado-1], nota_actual.octave)
					if grado_actual == intervalos[0]:
						nota_actual.octave_down()

				else:
					# se mantiene
					pass

				grado_actual = self.modo(self.tono.name).index(nota_actual.name) + 1
				pSubIni += cambioSub
				pBajIni += cambioBaj

				# ver si se debe sobreescribir o modificar
				r =random.random()
				if r < pMod:
					# se debe modificar
					if self.obtenerNota(c, t)[2]:
						grado_temp = self.modo(self.tono.name).index(self.obtenerNota(c, t).name)
						self.cambiarNota(c, t, self.modo(self.tono.name)[(grado_temp+mod)%7])
				else:
					self.cambiarNota(c, t, copiar.nota(nota_actual))
		return self

	def mezclar(self, track, pEscrIni, pEscrFin):
		""" mezclar el track dado con cierto porcentaje de escritura de forma inicial y final cambiando de forma gradual
		"""

		raise NameError('NoImplementadoTodavia')

	def mostrar(self):
		""" Muestra las notas de la secuencia
		"""

		for c in range(self.compases):
			for t in range(self.tiempo):
				if self.obtenerNota(c, t)[2]:
					sys.stdout.write(str(self.obtenerNota(c, t)[2][0]) + ' ')
				else:
					sys.stdout.write('x ')
			sys.stdout.write('| ')
		sys.stdout.write('\n')
		return self

	def tocar(self):
		""" hace sonar la secuencia
		"""

		fluidsynth.play_Track(self.track)
		return self

	def copiar(self):
		""" Entrega una copia del track
		"""

		rs = Secuencia(self.pulso, self.tiempo, self.compases, self.tono, self.modo)
		ct = Track()
		for c in range(self.compases):
			for t in range(self.tiempo):
				ct.add_notes(self.obtenerNota(c, t)[2], self.pulso)
		rs.track = ct
		return rs
