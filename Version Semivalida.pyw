import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QGraphicsScene 
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
		self.buscar.clicked.connect(self.getfile)
		self.scene = QGraphicsScene()
		#Buscar Imagen con explorer    
		
	#Abrir imagen
	def getfile(self):
		image_name = QFileDialog.getOpenFileName(self, 'Open File', '',"Image files (*.jpg *.png *.bmp)")
		self.rutaimg.setText(str(image_name[0]))
		img = QPixmap(image_name[0])
		img_original = cv2.imread(image_name[0],1)
		img_preprocesada = self.preprocesado(image_name[0],125,1)
		img_procesada = self.procesado(img_preprocesada, img_original)
		img_final = self.pintar(img_procesada)
		cv2.imwrite('img_final.png',img_final)
		img_final_pixmap = QPixmap("img_final.png")
		self.imagen.setPixmap(img_final_pixmap)
		self.imagen.show();
		
		
	def preprocesado(self, imgpath, umbral, erosionar):

		#Leer la Imagen
		img = cv2.imread(imgpath,1)

		#Desaturacion 
		gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		#Binarizacion con umbral adaptativo por el usuario
		ret,procesada = cv2.threshold(gray_image,umbral,255,cv2.THRESH_BINARY)
		kernel = np.ones((5,5), np.uint8)
		preprocesada = cv2.dilate(procesada,kernel,iterations = 1)
		return preprocesada
			
	def procesado(self,img_preprocesada, img_original):
		global array_contornos
		array_contornos = []
		global media_perimetro
		canny = cv2.Canny(img_preprocesada, 0, 255)
		(imagen, contornos, jerarquia) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for elemento in contornos:
				perimetro = perimetro+cv2.arcLenght(elemento,False)
				cv2.drawContours (img_original, contornos, -1, [0,0,0], 3)
				self.add_array(elemento, array_contornos)
		
		media_perimetro = self.calcular_media_perimetro(contornos, perimetro)
		print(media_perimetro)
		return img_original
		
	def pintar(self, img_original):
		count = 1
		for elemento in array_contornos:
			if cv2.arcLenght(elemento,False)<(media_perimetro+50) or cv2.arcLenght(elemento,False)>(media_perimetro-50):
				x,y,w,h = cv2.boundingRect(elemento)
				cv2.putText(img_original, str(count), (x,y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1,(0,255,0),2)
				count = count + 1
		cv2.putText(img_original, str(count-1),(50,50), cv2.
		FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,255,0),2)
		return img_original
		
	def add_array(self, elemento, array_contornos):
		array_contornos.append(elemento)
	
	def calcular_media_perimetro(self, contornos, perimetro):
		media_perimetro = perimetro/contornos.size()
		return media_perimetro
	#Instanciacion para iniciar app
app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()
