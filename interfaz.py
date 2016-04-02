#
# ALGORITMOS II - PROYECTO II
#
# REPRODUCTOR DE MUSICA
#
#				AUTORES:
#						- Jose Acevedo 13-10006
#						- Pablo Dario Betancourt 13-10147

# Modulos
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sys import *
from cliente import *

# Implementacion de la interfaz grafica del reproductor de musica
class Interfaz(QWidget):

	# Inicialzar ventana
	def __init__(self,reproductor,indiceGenero,indiceArtista,listaOriginal):
		super(Interfaz, self).__init__()
		self.setWindowTitle("JP Music Player")
		self.setFixedSize(400,600)
		self.reproductor = reproductor
		self.indiceArtista = indiceArtista
		self.indiceGenero = indiceGenero
		self.listaOriginal = listaOriginal
		palette = QPalette()
		palette.setBrush(QPalette.Background,QBrush(QPixmap("imagenes/fondo.jpg")))
		self.setPalette(palette)
		self.setWindowIcon(QIcon('imagenes/icono.jpg'))
		QFontDatabase.addApplicationFont("font/TTF files/Track.ttf")
		self.playClick = False
		
		# Cuadros de texto
		self.sonando = QLabel("Not playing   ",self)
		self.tituloCancionActual = QLabel("",self)
		self.artistaCancionActual = QLabel("",self)
		self.duracionCancionActual = QLabel("",self)
		self.tiempoTranscurridoCancionActual = QLabel("",self)
		self.barra = QLabel("",self)
		self.sonando.setStyleSheet("font-style: oblique; font-size: 10pt; font-family: Track; color:#2f4f4f;")
		self.tituloCancionActual.setStyleSheet("font-style: strong; font-size: 14pt; font-family: Track; color:#2f2f2f; margin:10px 10px 0px 10px;")
		self.artistaCancionActual.setStyleSheet("font-size: 11pt; font-family: Track; color:#2f3f3f; margin:0px 10px 10px 10px;")
		self.duracionCancionActual.setStyleSheet("font-size: 10pt; font-family: Track; color:#2f4f4f;")
		self.tiempoTranscurridoCancionActual.setStyleSheet("font-size: 10pt; font-family: Track; color:#2f4f4f;")

		# Botones
		self.pause      = QPushButton(" ",self)
		self.play       = QPushButton(" ",self)
		self.stop       = QPushButton(" ",self)
		self.atras      = QPushButton(" ",self)
		self.siguiente  = QPushButton(" ",self)

		# No sombrear botones
		self.play.setFocusPolicy(Qt.NoFocus)
		self.pause.setFocusPolicy(Qt.NoFocus)
		self.stop.setFocusPolicy(Qt.NoFocus)
		self.atras.setFocusPolicy(Qt.NoFocus)
		self.siguiente.setFocusPolicy(Qt.NoFocus)
		
		# Funcion a llamar cuando se hace click en botones
		self.connect(self.play,      SIGNAL("clicked()"),self._play)
		self.connect(self.pause,     SIGNAL("clicked()"),self._pause)
		self.connect(self.stop,      SIGNAL("clicked()"),self._stop)
		self.connect(self.atras,     SIGNAL("clicked()"),self._atras)
		self.connect(self.siguiente, SIGNAL("clicked()"),self._siguiente)

		# Diseno grafico de botones
		self.play.setStyleSheet("border: 0px; width: 50; height: 50; background-image: url(imagenes/play.svg); background-position: center; background-repeat: no-repeat")
		self.pause.setStyleSheet("border: 0px; width: 50; height: 50; background-image: url(imagenes/pause.svg); background-position: center; background-repeat: no-repeat")
		self.stop.setStyleSheet("border: 0px; width: 50; height: 50; background-image: url(imagenes/stop.svg); background-position: center; background-repeat: no-repeat")
		self.atras.setStyleSheet("border: 0px; width: 50; height: 50; background-image: url(imagenes/previous.svg); background-position: center; background-repeat: no-repeat")
		self.siguiente.setStyleSheet("border: 0px; width: 50; height: 50; background-image: url(imagenes/next.svg); background-position: center; background-repeat: no-repeat")

		# Bloque estructural de barra de botones
		self.barraDeBotones = QHBoxLayout()
		self.barraDeBotones.addWidget(self.atras)
		self.barraDeBotones.addWidget(self.stop)
		self.barraDeBotones.addWidget(self.play)
		self.barraDeBotones.addWidget(self.pause)
		self.barraDeBotones.addWidget(self.siguiente)

		# Bloque estructural de tabla de canciones
		self.tablaCanciones = QTableWidget()
		self.tablaCanciones.setColumnCount(1)
		self.tablaCanciones.verticalHeader().setVisible(False)
		self.tablaCanciones.horizontalHeader().setVisible(False)
		self.tablaCanciones.setShowGrid(False)
		self.tablaCanciones.setFocusPolicy(Qt.NoFocus)
		self.tablaCanciones.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaCanciones.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.tablaCanciones.setStyleSheet("background-color: transparent;");

		# Bloque estructural de cancion reproducida actualmente
		self.datos = QHBoxLayout()
		self.bloqueSonando = QHBoxLayout()
		self.tiempos = QHBoxLayout()
		self.tiempos.addStretch(1)
		self.tiempos.addWidget(self.tiempoTranscurridoCancionActual)
		self.tiempos.addWidget(self.barra)
		self.tiempos.addWidget(self.duracionCancionActual)
		self.tiempos.insertSpacing(3,10)
		self.tiempos.insertSpacing(2,10)
		self.aux  = QVBoxLayout()
		self.aux2 = QHBoxLayout()
		self.aux2.addStretch(1)
		self.aux2.addWidget(self.sonando)
		self.aux.addLayout(self.aux2)
		self.aux.addLayout(self.tiempos)
		self.bloqueSonando.addStretch(1)
		self.bloqueSonando.addLayout(self.aux)
		self.datosCancion = QVBoxLayout()
		self.datosCancion.addWidget(self.tituloCancionActual)
		self.datosCancion.addWidget(self.artistaCancionActual)
		self.datosCancion.insertSpacing(1,3)
		self.datos.addLayout(self.datosCancion)
		self.datos.addLayout(self.bloqueSonando)

		# Barra de recorrido de cancion
		self.barraCancion = Phonon.SeekSlider(self.reproductor.media)
		self.barraCancion.setStyleSheet("""
		QSlider::groove:horizontal { background: transparent; height: 20px;} 
		QSlider::sub-page:horizontal { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #66e, stop: 1 #bbf); background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #bbf, stop: 1 #55f); height: 20px;}
		QSlider::add-page:horizontal { background: transparent; height: 20px;}
		QSlider::handle:horizontal {background: transparent; border: 0px; width: 0px; margin-top: 0px; margin-bottom: 0px; border-radius: 0px;}""")

		# Tiempo de actualizacion de la interfaz
		self.reproductor.media.setTickInterval(1000)
		self.reproductor.media.tick.connect(self.actualizar)

		# Layout principal de la ventana
		self.layoutPrincipal = QVBoxLayout()
		self.layoutPrincipal.addLayout(self.datos)
		self.layoutPrincipal.addWidget(self.tablaCanciones)
		self.layoutPrincipal.addWidget(self.barraCancion)
		self.layoutPrincipal.addLayout(self.barraDeBotones)
		self.setLayout(self.layoutPrincipal)
		self.layoutPrincipal.insertSpacing(0,10)
		self.layoutPrincipal.insertSpacing(2,10)

		# Mostra lista de reproduccion
		self.cargarListaReproduccion(listaOriginal)

	# Funcion que reproduce cancion
	def _play(self):
		self.reproductor.Play()
		self.cambiarDatosCancionActual()
		self.sonando.setText("Now playing   ")
		self.playClick = True
	# Funcion que pausa cancion
	def _pause(self):
		self.reproductor.Pause()
		self.sonando.setText("Paused    ")
		self.playClick = False
	# Funcion que detiene archivo de audio
	def _stop(self):
		self.reproductor.Stop()
		self.playClick = False
	# Funcion que retrocede a cancion previa de la lista de reproduccion
	def _atras(self):
		self.reproductor.Atras()
		self.cambiarDatosCancionActual()
		self.sonando.setText("Now playing   ")
	# Funcion que pasa a la siguiente cancion de la lista de reproduccion y la reproduce
	def _siguiente(self):
		self.reproductor.Siguiente()
		self.cambiarDatosCancionActual()
		self.sonando.setText("Now playing   ")
	# Fucion que actualiza el panel de datos de la cancion que se reproduce actualmente		
	def cambiarDatosCancionActual(self):
		self.tituloCancionActual.setText(self.reproductor.cancionActual.cancion.titulo)
		self.artistaCancionActual.setText(self.reproductor.cancionActual.cancion.artista)

	# Funcion que llena la tabla grafica con la lista de reproduccion
	def cargarListaReproduccion(self,lista):
		self.tablaCanciones.setRowCount(lista.size)
		node = lista.head
		for i in range(lista.size):
			item = QLabel("<br><b>"+str(i+1)+". "+node.cancion.titulo+"</b><br><small><span style='margin:10px 5px 15px 20px;'>"+node.cancion.artista+"<br>"+node.cancion.genero+"</span></small><br>")
			item.setContentsMargins(15,0,15,0)
			item.setStyleSheet('font-size: 10pt; font-family: Track; color:#2f4f4f;')
			self.tablaCanciones.setCellWidget(i,0,item)
			node = node.next
		self.tablaCanciones.resizeRowsToContents()

	# Actualizar contador de tiempo transcurrido desde inicio de cancion
	def actualizar(self, time):	
		tiempoTranscurrido = self.reproductor.media.currentTime()
		tiempo1 = QTime(0, (tiempoTranscurrido / 60000) % 60, (tiempoTranscurrido / 1000) % 60)
		tiempo2 = QTime(0, (self.reproductor.media.totalTime() / 60000) % 60, (self.reproductor.media.totalTime() / 1000) % 60)
		self.tiempoTranscurridoCancionActual.setText(tiempo1.toString('mm:ss'))
		self.duracionCancionActual.setText(tiempo2.toString('mm:ss'))
		self.barra.setText("/")

	# Determina si hay un archivo de audio reproduciendose actualmente
	def seEstaReproduciendoMusica(self):
		return self.playClick

	# Funcion para activar y desactivar panel grafico
	def administrarInterfazGrafica(self,flag):
		self.pause.setEnabled(flag)
		self.play.setEnabled(flag)
		self.stop.setEnabled(flag)
		self.atras.setEnabled(flag)
		self.siguiente.setEnabled(flag)

	# Funcion que maneja los eventos de la aplicacion
	def keyPressEvent(self, event):
		# Si se preciona ENTER entonces se intercambia
		# entre ventana grafica y consola de texto
		if event.key() == Qt.Key_Return:
			if not self.seEstaReproduciendoMusica():
				estadoConsola(True)
				self.administrarInterfazGrafica(False)
				menuConsola(self)
				QCoreApplication.processEvents()
				self.administrarInterfazGrafica(True)
				estadoConsola(False)
			else:
				advertenciaConsola()