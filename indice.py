#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# Modulos
# Modulo que contiene funcion de hash para utilizar en la tabla de hash
from fnvhash import fnv1a_32 as fm 
from listaReproduccion import *

# Elemento de la tabla de Hash. Los elementos
# contienen una clave que puede ser un nombre de artista
# o un genero. Los datos satelite son una lista enlazada
# con todas las canciones cuyo artista o genero sea
# el indicado por la clave
class nodoIndice:
	def __init__(self,clave,lista):
		self.clave = clave
		self.lista = lista
		self.next = None
		self.prev = None

# Implementacion de una lista doblemente enlazada
class dlist:
	def __init__(self):
		self.head = None

	# Inserta elementos al frente de la lista
	def insert(self,node):
		node.next = self.head
		if self.head != None:
			self.head.prev = node
		self.head = node

	# Dada una clave la cual puede ser o un artista o un genero
	# se retorna la lista con las canciones cuyo artista o
	# genero sea igual a la clave
	def search(self, clave):
		node = self.head
		while node != None and node.clave.lower() != clave.lower():
			node = node.next
		return node

# Implementacion de un indice musical con una tabla de hash
# Dado un artista se retorna todas las canciones cuyo artista sea
# el especificado. De igual forma, dado un genero se retornan
# todas las canciones pertenecientes a dicho genero
class Indice:
	# Constructor:
	# Se crea una tabla de hash de tamano inicial 5
	def __init__(self,size = 5):
		self.size = size
		self.slot = [dlist() for i in range(self.size)]
		self.nodes = 0

	# Funcion de hash de la tabla de hash
	def fh(self,clave):
		return fm(clave.lower())%self.size

	# Funcion de rehash: Cuando el factor de carga excede
	# el 80% entonces el tamano de la tabla se duplica
	def rehash(self):
		N = self.size
		A = list(self.slot)
		self.size = 2*self.size + 1
		self.slot = [ dlist() for i in xrange(self.size) ]
		self.nodes = 0
		for i in xrange(N):
			x = A[i].head
			while x!=None:
				self.insertNode(x)
				x = x.next

	# Insercion de un elemento en la tabla de hash
	# Se calcula indice por medio de la funcion de hash
	# y y anade a la lista correspondiente.
	# El factor de carga se actualiza
	def insertNode(self, node):
		m = self.fh(node.clave)
		x = self.slot[m].search(node.clave)
		if x == None:
			self.slot[m].insert(node)
			self.nodes += 1
		else:
			x.lista.agregar_final(node.lista.head.cancion)
		if (float(self.nodes)/self.size)*100 >= 80:
			self.rehash()

	# Permite insertar una cancion en una tabla de hash
	# cuyas claves son los nombres de los artistas
	def insertArtista(self,cancion):
		l = listaReproduccion()
		l.agregar(cancion)
		node = nodoIndice(cancion.artista,l)
		self.insertNode(node)

	# Permite insertar una cancion en una tabla de hash
	# que representa un indice por genero dado el genero
	# de la cancion a insertar
	def insertGenero(self,cancion):
		l = listaReproduccion()
		l.agregar(cancion)
		node = nodoIndice(cancion.genero,l)
		self.insertNode(node)

	# Dada una clave se retornan las canciones asociadas
	# a dichas claves. Se puede buscar por artista
	# o por genero musical
	def search(self,clave):
		m = self.fh(clave)
		x = self.slot[m].search(clave)
		if x != None : return x.lista