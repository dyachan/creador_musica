#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from mingus.containers.Bar import Bar
from mingus.containers.Track import Track

import mingus.core.notes as _notes
import mingus.core.scales as _scales

class Secuencia:
	""" clase que controla una secuencia de notas.
	"""

	class ESCALA:
		ionian = _scales.ionian
		dorian = _scales.dorian
		phrygian = _scales.phrygian
		lydian = _scales.lydian
		mixolydian = _scales.mixolydian
		aeolian = _scales.aeolian
		locrian = _scales.locrian

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
		for _ in range(compases):
			self.track = buffBar.deepcopy()

		self.modo = modo(self.tono)

	def obtenerNota(self, compas, tiempo):
		"""	obtener un arreglo de notas que representan en el mismo orden las notas de las posiciones solicitadas
		"""

		return self.track[compas][tiempo]

	def agregarTrack(self, track):
		""" agrega el track dado al de la secuencia 
		"""

		raise NoImplementadoTodavia, "Funcionalidad no implementada todavía"

	def cortarInicio(self, compases):
		""" elimina la cantidad de compases elegidos del inicio de la secuencia
		"""

		raise NoImplementadoTodavia, "Funcionalidad no implementada todavía"

	def cortarfinal(self, compases):
		""" elimina la cantidad de compases elegidos del final de la secuencia
		"""

		raise NoImplementadoTodavia, "Funcionalidad no implementada todavía"

	def invertir(self):
		""" invierte la secuencia
		"""

		raise NoImplementadoTodavia, "Funcionalidad no implementada todavía"

	def cambiarTono(self, tono):
		""" cambia la tonal de la secuencia
		"""

		tonoViejo = self.tono.deepcopy()
		self.tono = tono

		if _notes.note_to_int(tonoViejo) > _notes.notes_to_int(tono):
			tono = int_to_note(12-_notes.note_to_int(tono))
		intervalo = _notes.notes_to_int(tono) - _notes.notes_to_int(tonoViejo)

		for compas in self.track[:]:
			for notas in compas[:]:
				for nota in notas[:]:
					for _ in range(intervalo):
						nota.augment()

	def cabiarModo(self, modo):
		""" cambia el modo de la secuencia
		"""

		modoViejo = self.modo.deepcopy()
		self.modo = modo

		notas_de_modo = modoViejo.ascending()
		for compas in self.track[:]:
			for notas in compas[:]:
				for nota in notas[:]:
					nota = self.modo.degree(notas_de_modo.index(nota))

	def magiarSecuencia(self, nota, pSubIni, pSubfin, pBajIni, pBajFin, pMod, intervalos):
		""" crea una secuencia partiendo de una nota; subiendo, bajando o manteniendo la tonalidad con un cierto porcentaje al inicio y al final cambiando de forma gradual; con cierta probabilidad de modificar la nota por sobreescribirla; para un conjunto de intervalos permitidas
		"""

		#while current_beat < 1:
		pass

	def mezclar(self, track, pEscrIni, pEscrFin):
		""" mezclar el track dado con cierto porcentaje de escritura de forma inicial y final cambiando de forma gradual
		"""

		pass

