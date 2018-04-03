import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#Clase Heredada WMainWindow (Constructor de Ventanas)

class Ventana(QMainWindow):
	
	#Constructor
	def __init__(self):
            
	    #Inicializar MainWindow
	    QMainWindow.__init__(self)
	    #Cargar configuracion de la UI
	    uic.loadUi("MainWindow.ui",self)
	    
	    self.buscar.clicked.connect(self.mostrar_img)

	    


        #Evento Boton Buscar (Click)
	def mostrar_img(self):
                  self.imagen.setPixmap(QPixmap("image.jpg"))
                  self.imagen.show();
                


	#Instanciacion para iniciar app
app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()

