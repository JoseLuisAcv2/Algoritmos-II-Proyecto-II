#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# TAD Lista de reproduccion. Implementado con lista circular doblemente enlazada
# Modulo
from cancion import *
# Clase para nodos de la lista enlaada
class nodoLista:
	# Constructor:
	# Un nodo tiene apuntador al siguiente, al anterior y los datos satelites con la informacion de la cancion
	def __init__(self,cancion):
		self.cancion = cancion
		self.prev = None
		self.next = None

# Implementacion del TAD Lista de Reproduccion
class listaReproduccion:
	# Constructor:
	# Se implementa con una lista enlazada. Inicialmente vacia
	def __init__(self):
		self.head = None
		self.size = 0

	# Funcion para agregar canciones a la lista de reproduccion
	def agregar(self,cancion):
		node = nodoLista(cancion)
		if self.head == None:
			node.next = node
			node.prev = node
			self.head = node
			self.size += 1
		else:
			if self.buscar(cancion) == None:
				node.next = self.head
				self.head.prev.next = node
				node.prev = self.head.prev
				self.head.prev = node
				self.head = node
				self.size+=1

	# Funcion para agregar canciones a la lista de reproduccion al final de la lista
	def agregar_final(self,cancion):
		node = nodoLista(cancion)
		if self.head == None:
			node.next = node
			node.prev = node
			self.head = node
			self.size += 1
		else:
			if self.buscar(cancion) == None:
				self.head.prev.next = node
				node.prev = self.head.prev
				self.head.prev = node
				node.next = self.head
				self.size+=1

	# Funcion para buscar si una determinada cancion se encuentra en la lista de reproduccion
	# En caso de estar presente retorna un apuntador a la cancion. En caso contrario retorna None
	def buscar(self,cancion):
		x = self.head
		for i in xrange(self.size):
			if x.cancion.esIgual(cancion) : return x
			x = x.next
		return None

	# Funcion que recibe una cancion y la elimina de la lista de reproduccion
	def eliminar(self,cancion):
		x = self.buscar(cancion)
		if x != None:
			x.prev.next = x.next
			x.next.prev = x.prev
			if x == self.head : self.head = x.next
			self.size-=1

	# Funcion que compara dos TADs cancion.
	# Se pueden comparar por titulo de cancion o por artista de cancion
	def comp(self,a,b,c):
		# Comparar por titulo
		if c == 0:
			return a.cancion.esMenorTitulo(b.cancion)
		# Comparar por artista
		else:
			return a.cancion.esMenorArtista(b.cancion)


	# Funcion que ordena la lista de reproduccion por orden lexicografico del titulo
	# de las canciones. Para ordenar la lista se utiliza el algoritmo Mergesort
	def ordenarTitulo(self):
		self.head.prev.next = None
		self.head.prev = None
		self.head = self.mergesort(self.head,0)
		x = self.head
		while x!=None and x.next != None: 
			x = x.next
		self.head.prev = x
		x.next = self.head

	# Funcion que ordena la lista de reproduccion por orden lexicografico del artista
	# de las canciones. Para ordenar la lista se utiliza el algoritmo Mergesort
	def ordenarArtista(self):
		self.head.prev.next = None
		self.head.prev = None
		self.head = self.mergesort(self.head,1)
		x = self.head
		while x!=None and x.next != None: 
			x = x.next
		self.head.prev = x
		x.next = self.head

	# Algoritmo Mergesort para ordenar la lista de reproduccion
	def mergesort(self,head,flag):
		if head == None or head.next == None:
			return head
		second = self.split(head)
		head = self.mergesort(head,flag)
		second = self.mergesort(second,flag)
		return self.merge(head,second,flag)

	# Sub procedimiento de Mergesort para hacer merge de dos
	# listas enlazadas
	def merge(self,head,second,flag):
		if head == None : return second
		if second == None : return head

		if self.comp(head,second,flag):
			head.next = self.merge(head.next,second,flag)
			head.next.prev = head
			head.prev = None
			return head
		else:
			second.next = self.merge(head,second.next,flag)
			second.next.prev = second
			second.prev = None
			return second

	# Sub procedimiento de Mergesort para dividir una lista
	# enlazada en dos listas enlazadas
	def split(self,head):
		fast = head
		slow = head
		while fast.next != None and fast.next.next != None:
			fast = fast.next.next
			slow = slow.next
		tmp = slow.next
		slow.next = None
		return tmp