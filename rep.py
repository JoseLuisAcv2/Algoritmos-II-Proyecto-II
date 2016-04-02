#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# Modulos requeridos
from PyQt4.QtGui import *
from PyQt4.phonon import *
from listaReproduccion import *

# Implementacion del TAD reproductor haciendo uso
# de la libreria de audio Phonon perteneciente a PyQt4
class Reproductor:
	# Constructor:
	# Se crea un objeto media para reproducir archivos de audio
	# Estos archivos de audio pertenecen a una lista de reproduccion
	# Y se mantiene un apuntador a la cancion que esta siendo reproducida
	# actualmente
	def __init__(self):
		self.media = Phonon.MediaObject()
		self.lista = None
		self.cancionActual = None
		self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
		Phonon.createPath(self.media, self.audioOutput)
	# Funcion para reproducir y escuchar audio
	def Play(self):
		self.media.play()
	# Funcion para pausar archivo de audio
	def Pause(self):
		self.media.pause()
	# Funcion para detener archivo de audio
	def Stop(self):
		self.media.stop()
	# Funcion para pasar a la siguiente cancion dentro de la
	# lista de reproduccion y reproducirla
	def Siguiente(self):
		self.Stop()
		self.cancionActual = self.cancionActual.next
		self.media.setCurrentSource(Phonon.MediaSource(self.cancionActual.cancion.archivo))
		self.Play()
	# Funcion para retroceder a la cancion anterior en la
	# lista de reproduccion y reproducirla
	def Atras(self):
		self.Stop()
		self.cancionActual = self.cancionActual.prev
		self.media.setCurrentSource(Phonon.MediaSource(self.cancionActual.cancion.archivo))
		self.Play()
	# Funcion para establecer una lista de reproduccion
	def setLista(self,lista):
		self.lista = lista
		self.cancionActual = self.lista.head
		self.media.setCurrentSource(Phonon.MediaSource(self.cancionActual.cancion.archivo))