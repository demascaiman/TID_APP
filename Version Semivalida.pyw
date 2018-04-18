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
		self.buscar.clicked.connect(self.main)
		self.recalc_button.clicked.connect(self.reestart)
		self.del_button.clicked.connect(self.borrar)
		self.add_button.clicked.connect(self.add_number)
		self.save_button.clicked.connect(self.savefile)
		self.umbral_sli.valueChanged.connect(self.slider_actus)
		self.erosion_sli.valueChanged.connect(self.slider_actus)
		self.perimetro_sli.valueChanged.connect(self.slider_actus)
		self.slider_actus()
		#Buscar Imagen con explorer    
		
	#Abrir imagen
	def getfile(self):
		image_name = QFileDialog.getOpenFileName(self, 'Open File', '',"Image files (*.jpg *.png *.bmp)")
		self.rutaimg.setText(str(image_name[0]))
		
		return image_name
		
	def slider_actus(self):
		umbra_val = self.umbral_sli.value()
		perimetro_val = self.perimetro_sli.value()
		erosion_val = self.erosion_sli.value()
		self.erosion_label.setText(str(erosion_val))
		self.umbral_label.setText(str(umbra_val))
		self.perimetro_label.setText(str(perimetro_val))
		
	def savefile(self):
		nombre_fichero = QFileDialog.getSaveFileName(self, "Guardar fichero","img_final.png")
		img_final = cv2.imread("img_final.png",1)
		
		cv2.imwrite(nombre_fichero[0],img_final)
	def reestart(self):
		if self.rutaimg.text() != "":
			ruta_image = self.rutaimg.text()
			img_original = cv2.imread(ruta_image,1)
			img_preprocesada = self.preprocesado(ruta_image,self.umbral_sli.value(),1)
			img_procesada = self.procesado(img_preprocesada, img_original)
			cv2.imwrite('img_procesada.png', img_procesada)
			img_final = self.pintar(img_procesada)
			cv2.imwrite('img_final.png',img_final)
			img_final_pixmap = QPixmap("img_final.png")
			self.imagen.setPixmap(img_final_pixmap)
			self.imagen.show();
	
	def main(self):
		image_name = self.getfile()	
		img_original = cv2.imread(image_name[0],1)
		img_preprocesada = self.preprocesado(image_name[0],self.umbral_sli.value(),1)
		img_procesada = self.procesado(img_preprocesada, img_original)
		cv2.imwrite('img_procesada.png', img_procesada)
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
		preprocesada = cv2.dilate(procesada,kernel,iterations = self.erosion_sli.value())
		return preprocesada
			
	def procesado(self,img_preprocesada, img_original):
		global array_contornos
		array_contornos = []
		perimetro = 0
		canny = cv2.Canny(img_preprocesada, 0, 255)
		(imagen, contornos, jerarquia) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for elemento in contornos:
				cv2.drawContours (img_original, contornos, -1, [0,0,0], 3)
				self.add_array(elemento, array_contornos)
		return img_original
		
	def pintar(self, img_original):
		count = 1
		mod_array = self.mod_array(array_contornos)
		for elemento in mod_array:			
			cv2.putText(img_original, str(count), elemento, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1,(0,255,0),2)
			count = count + 1
		self.count.setText(str(count-1))
		return img_original
		
	def add_array(self, elemento, array_contornos):
		array_contornos.append(elemento)
		
	def mod_array(self, array_contornos):
		global array_xy
		array_xy = []
		for elemento in array_contornos:
			if cv2.arcLength(elemento,False)>self.perimetro_sli.value():
				x,y,w,h = cv2.boundingRect(elemento)
				array_xy.append((x,y))
		return array_xy
	def borrar(self):
		global array_xy
		if int(self.index_del.toPlainText()) > 0 and int(self.index_del.toPlainText()) < len(array_xy):
			num = int(self.index_del.toPlainText())
			array_xy[num-1] = (-1,-1)
			img_aux = cv2.imread('img_procesada.png',1)
			img_final = self.pintar2(img_aux)
			cv2.imwrite('img_final.png',img_final)
			img_final_pixmap = QPixmap("img_final.png")
			self.imagen.setPixmap(img_final_pixmap)
			self.imagen.show();
			
	def esta_es_muy_cerda(self, array_xy):
		global array_aux
		array_aux = []
		num = (int(self.index_del.toPlainText())-1)
		for element in array_xy:
			if element == array_xy[num]:
				array_aux.append((-1,-1))
			else:
				array_aux.append(element)
		return array_aux	

	def pintar2(self, img_original):
		count = 0
		mod_array = self.esta_es_muy_cerda(array_xy)
		contador = 1
		for elemento in mod_array:	
			if elemento != (-1,-1):
				cv2.putText(img_original, str(contador), elemento, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1,(0,255,0),2)
				count = count + 1
			contador = contador + 1
		self.count.setText(str(count))
		return img_original
	def add_number(self):
		img_final_pixmap = QPixmap("img_final.png")
		self.imagen.setPixmap(img_final_pixmap)
		self.imagen.mousePressEvent = self.getPixel
		img_aux = cv2.imread('img_procesada.png',1)
		img_final = self.pintar3(img_aux)
		cv2.imwrite('img_final.png',img_final)
		img_final_pixmap = QPixmap("img_final.png")
		self.imagen.setPixmap(img_final_pixmap)
		self.imagen.show();
		
		
	def getPixel(self, event):
		global array_xy
		x = event.pos().x()
		y = event.pos().y()
		self.x_pos.setText(str(x))
		self.y_pos.setText(str(y))
		array_xy.append((x,y))
		
	def pintar3(self, img_original):
		count = 0
		contador = 1
		for elemento in array_xy:
			if elemento != (-1,-1):
				cv2.putText(img_original, str(contador), elemento, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1,(0,255,0),2)
				count = count + 1
			contador = contador + 1
		self.count.setText(str(count))
		return img_original
			
	#Instanciacion para iniciar app
app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()
