#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# Modulos para ejecutar aplicacion
from rep import *
from cliente import *
from interfaz import *

if __name__ == '__main__':
	# Verificar que archivo con canciones haya sido incluido
	if len(argv) != 2:
		print "FATAL ERROR:"
		print "> python reproductor.py <archivo>"
		exit()

	# Inicializar PyQt4
	app = QApplication([])
	app.setApplicationName("JP Music Player")
	# Inicializar estructuras fundamentales del reproductor
	(reproductor,indiceGenero,indiceArtista,listaOriginal) = initCliente(argv[1])
	# Inicializar interfaz grafica
	ventana = Interfaz(reproductor,indiceGenero,indiceArtista,listaOriginal)
	# Mostrar ventana grafica
	ventana.show()
	pyqtRemoveInputHook()
	exit(app.exec_())