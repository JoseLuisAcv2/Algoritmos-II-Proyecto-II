#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# TAD CANCION
class Cancion:
	# Constructor
	# Asigna atributos: titulo, artista, genero y archivo de audio de la cancion
	def __init__(self,titulo,artista,genero,archivo):
		self.titulo = titulo
		self.artista = artista
		self.genero = genero
		self.archivo = archivo
	# Determina si la cancion es igual a otra cancion.
	# Dos canciones son igual si su titulo es igual y su artista es igual
	def esIgual(self,cancion):
		return self.titulo.lower() == cancion.titulo.lower() and self.artista.lower() == cancion.artista.lower()
	# Determina si la cancion es menor a otra con respecto al artista.
	# Una cancion es menor a otra si su nombre de artista es menor o sus nombres de artistas son iguales y su titulo es menor
	def esMenorArtista(self,cancion):
		return self.artista.lower() < cancion.artista.lower() or(self.artista.lower() == cancion.artista.lower()  and self.titulo.lower() <= cancion.titulo.lower())
	# Determina si la cancion es menor a otra con respecto al titulo.
	# Una cancion es menor a otra si su titulo es menor o sus titulos son iguales y su nombre de artista es menor
	def esMenorTitulo(self,cancion):
		return self.titulo.lower() < cancion.titulo.lower() or(self.titulo.lower() == cancion.titulo.lower()  and self.artista.lower() <= cancion.artista.lower())
	# Retorna titulo de la cancion
	def getTitulo(self):
		return self.titulo
	# Retorna genero de la cancion
	def getGenero(self):
		return self.genero
	# Retorna artista de la cancion
	def getArtista(self):
		return self.artista
	# Retorna archivo de la cancion
	def getArchivo(self):
		return self.archivo