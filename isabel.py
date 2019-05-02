import numpy as np
import cv2,os,time,math,random,sys
from ConfigParser import SafeConfigParser

class vision(object):
	def __init__(self):
		self.imagen=[]
		self.elementos_hpk=["Cinta roja","Cinta negra","Rosenberger rojo","Sello"]
		self.elementos_dcs=["Cinta roja","Candado rojo","Candado negro","Goma","Cover","Anillo"]
		self.cargar_configuraciones()

	def neurona(self,entrada): 
		mensajes,cuenta=[],0
		if self.configuracion=="DCS":
			l1 = self.sigmoid(np.dot(entrada, self.capa_1))
			l2 = self.sigmoid(np.dot(l1, self.capa_2))
			l2[0]=round(l2[0])
			if l2[0]==0:
				cuenta+=1
				mensajes.append("Falla en candado")
			for i in range(3,5):
				if self.autosalidas[i]==0:
					cuenta+=1
					mensajes.append("Falta "+self.elementos_dcs[i])
			if self.autosalidas[5]>0.2:
				cuenta+=1
				mensajes.append("Falta "+self.elementos_dcs[5])
		else:
			l1 = self.sigmoid(np.dot(entrada, self.capa_1))
			l2 = self.sigmoid(np.dot(l1, self.capa_2))
			l2[0]=round(l2[0])
			if l2[0]==0:
				cuenta+=1
				mensajes.append("Falla en rosenberger")
			if self.autosalidas[3]==0:
				cuenta+=1
				mensajes.append("Falta "+self.elementos_hpk[3])
		if cuenta>0:
			return mensajes
		elif cuenta==0:
			mensajes.append("Harness correcto")
			return mensajes

	def cabecera(self):
		print "_________________________________________"
		print "Detector de componentes - Isabel v0.80.3"
		print "Configuracion: ", self.configuracion
		print "Ciclos de aprendizaje obtenidos:  ", self.ciclos
		print "_________________________________________"

	def cargar_configuraciones(self):
		parser = SafeConfigParser()
		parser.read('./Datos/config.cfg')
		self.pesos_elementos,self.tolerancias,self.errores,self.capa_1,self.capa_2=[],[],[],[[],[],[]],[[]]
		self.rangos,valores=[],[]
		self.configuracion=parser.get('general','cable')
		paso=0
		for opcion, valor in parser.items('rangos'):
			valores.append(int(valor))
			paso+=1
			if paso==3:
				self.rangos.append(np.array(valores))
				valores,paso=[],0

		self.rangos_minus={"Cable":self.rangos[0],"Cinta Roja":self.rangos[2],"Cinta Negra":self.rangos[4],"Rosenberger Rojo":self.rangos[6],"Candado Rojo":self.rangos[8],"Candado Negro":self.rangos[10],"Cover":self.rangos[12],"Goma":self.rangos[14]}
		self.rangos_mayus={"Cable":self.rangos[1],"Cinta Roja":self.rangos[3],"Cinta Negra":self.rangos[5],"Rosenberger Rojo":self.rangos[7],"Candado Rojo":self.rangos[9],"Candado Negro":self.rangos[11],"Cover":self.rangos[13],"Goma":self.rangos[15]}

		if self.configuracion=="DCS":
			self.ciclos=parser.getint('general','ciclos_dcs')
			self.error=parser.getfloat('general','error_dcs')
			for opcion, valor in parser.items('dcs'):
				self.pesos_elementos.append(float(valor))
			for opcion, valor in parser.items('tolerancia_dcs'):
				self.tolerancias.append(int(valor))
			paso,cuenta=0,0
			for opcion, valor in parser.items('pesos_candado'):
				self.capa_1[cuenta].append(float(valor))
				paso+=1
				if paso==4:
					paso=0
					cuenta+=1
			for opcion, valor in parser.items('pesos_2_candado'):
				self.capa_2[0].append(float(valor))
		else:
			self.ciclos=parser.getint('general','ciclos_hpk')
			self.error=parser.getfloat('general','error_hpk')
			for opcion,valor in parser.items('hpk'):
				self.pesos_elementos.append(float(valor))
			for opcion,valor in parser.items('tolerancia_hpk'):
				self.tolerancias.append(int(valor))
			paso,cuenta=0,0
			for opcion, valor in parser.items('pesos_rosen'):
				self.capa_1[cuenta].append(float(valor))
				paso+=1
				if paso==4:
					paso=0
					cuenta+=1
			for opcion, valor in parser.items('pesos_2_rosen'):
				self.capa_2[0].append(float(valor))
		self.capa_1=np.array(self.capa_1)
		self.capa_2=np.array(self.capa_2).T

	def conteo_pixeles(self,imagen,c_menor,c_mayor):
		blancos=0
		#alto, ancho = imagen.shape[:2]
		for i in range(c_menor[0],c_mayor[0]):
			for ii in range(c_menor[1],c_mayor[1]):
				if imagen[i][ii]==255:
					blancos+=1
		return blancos

	def detectar_componente(self,imagen,componente,c_menor,c_mayor):
		return self.conteo_pixeles(cv2.inRange(imagen,componente[0],componente[1]),c_menor,c_mayor)

	def detectar_componentes(self,componentes):
		datos=[]
		for componente in componentes:
			datos.append(self.conteo_pixeles(cv2.inRange(self.imagen,componente[0],componente[1])))
		return datos

	def cargar_imagen(self,direccion,factor_dimension):
		self.imagen=cv2.imread(direccion)
		dim = (int(factor_dimension), int(self.imagen.shape[0] * (factor_dimension / self.imagen.shape[1])))
		self.imagen = cv2.resize(self.imagen, dim, interpolation = cv2.INTER_AREA)

	def sigmoid(self,x, deriv=False):
		if deriv:
			return x*(1-x)
		return 1/(1+np.exp(-x))

	def entrenamiento_manual(self,iteracion=False):
		if iteracion:
			print "____________________________"
			print "Pesos:    ",self.pesos_elementos
			for i in range(len(self.autosalidas)):
				if (self.autosalidas[i]<0.20 and self.autosalidas[i]>-0.10) or (self.autosalidas[i]<1.10 and self.autosalidas[i]>0.90):
					pass
				else:
					self.pesos_elementos[i]=self.pesos_elementos[i]-self.autosalidas[i]

			print "Pesos:    ",self.pesos_elementos
			print "____________________________"
			self.ciclos+=1 

			parser,paso= SafeConfigParser(),0
			parser.read('./Datos/config.cfg')
			if self.configuracion=="DCS":
				parser.set('general', 'ciclos_dcs', str(self.ciclos))
				for opcion,_ in parser.items('dcs'):
					parser.set('dcs', opcion, str(self.pesos_elementos[paso]))
					paso+=1
			else:
				parser.set('general', 'ciclos_hpk', str(self.ciclos))
				for opcion,_ in parser.items('hpk'):
					parser.set('hpk', opcion, str(self.pesos_elementos[paso]))
					paso+=1

			f = open("./Datos/config.cfg", "w")  
			parser.write(f)
			f.close()  
			self.cargar_configuraciones()
			return "[Isabel]: Cambios en IA realizados"
		else:
			return "[Isabel]: No se requirio cambios"

	def entrenamiento_autonomo(self,piezas_entrenamiento,elementos):
		os.system("clear") 
		self.cabecera()
		iteraciones=input("Numero de iteraciones: \nRespuesta:\t")
		os.system("clear") 
		self.cabecera()
		for i in range(iteraciones):
			harness,self.autosalidas=random.randint(3,4),[]
			print piezas_entrenamiento[harness][0][0]
			self.cargar_imagen(piezas_entrenamiento[harness][0][0],500.0)
			self.detector()
			for ii in range(elementos):
				self.salida=piezas_entrenamiento[harness][1][0][ii]
				self.autosalida=float(self.entrada[ii][0])/float(self.pesos_elementos[ii])
				self.autosalidas.append(self.autosalida)
				if (self.autosalida<0.20 and self.autosalida>-0.10) or (self.autosalida<1.10 and self.autosalida>0.90):
					pass
				else:
					diferencia=self.autosalida-self.salida
					self.error+=abs(diferencia)
					if diferencia!=0:
						self.pesos_elementos[ii]=self.pesos_elementos[ii]+diferencia
						self.autosalida=self.entrada[ii][0]/self.pesos_elementos[ii]
					print "ERROR:     ",abs(diferencia)
					print "_______________"
			print "Salida real:   ",piezas_entrenamiento[harness][1][0]
			print "_______________"
			print "Salida generada:    ",self.autosalidas
			print "_______________"
			print "Pesos:    ",self.pesos_elementos
			print "____________________________"
			self.error=piezas_entrenamiento[harness][1][0]-self.autosalidas
			print "Error general:   ", self.error
			self.ciclos+=1
			print "*****************************"

		parser,paso= SafeConfigParser(),0
		parser.read('./Datos/config.cfg')
		if self.configuracion=="DCS":
			parser.set('general', 'ciclos_dcs', str(self.ciclos))
			for opcion,_ in parser.items('dcs'):
				parser.set('dcs', opcion, str(self.pesos_elementos[paso]))
				paso+=1
		else:
			parser.set('general', 'ciclos_hpk', str(self.ciclos))
			for opcion,_ in parser.items('hpk'):
				parser.set('hpk', opcion, str(self.pesos_elementos[paso]))
				paso+=1

		f = open("./Datos/config.cfg", "w")  
		parser.write(f)
		f.close()  
		self.cargar_configuraciones()

	def entrenamiento(self,piezas_entrenamiento,elementos):
		os.system("clear") 
		self.cabecera()
		iteraciones=input("Numero de iteraciones: \nRespuesta:\t")
		os.system("clear") 
		self.cabecera()
		for i in range(iteraciones):
			harness,self.autosalidas=random.randint(3,4),[]
			print piezas_entrenamiento[harness][0][0]
			self.cargar_imagen(piezas_entrenamiento[harness][0][0],500.0)
			self.detector()
			for ii in range(elementos):
				self.salida=piezas_entrenamiento[harness][1][0][ii]
				self.autosalida=float(self.entrada[ii][0])/float(self.pesos_elementos[ii])
				self.autosalidas.append(self.autosalida)
				if (self.autosalida<0.20 and self.autosalida>-0.10) or (self.autosalida<1.10 and self.autosalida>0.90):
					pass
				else:
					diferencia=self.autosalida-self.salida
					self.error+=abs(diferencia)
					if diferencia!=0:
						self.pesos_elementos[ii]=self.pesos_elementos[ii]+diferencia
						self.autosalida=self.entrada[ii][0]/self.pesos_elementos[ii]
					print "ERROR:     ",abs(diferencia)
					print "_______________"
			print "Salida real:   ",piezas_entrenamiento[harness][1][0]
			print "_______________"
			print "Salida generada:    ",self.autosalidas
			print "_______________"
			print "Pesos:    ",self.pesos_elementos
			print "____________________________"
			self.error=piezas_entrenamiento[harness][1][0]-self.autosalidas
			print "Error general:   ", self.error
			self.ciclos+=1
			print "*****************************"

		parser,paso= SafeConfigParser(),0
		parser.read('./Datos/config.cfg')
		if self.configuracion=="DCS":
			parser.set('general', 'ciclos_dcs', str(self.ciclos))
			for opcion,_ in parser.items('dcs'):
				parser.set('dcs', opcion, str(self.pesos_elementos[paso]))
				paso+=1
		else:
			parser.set('general', 'ciclos_hpk', str(self.ciclos))
			for opcion,_ in parser.items('hpk'):
				parser.set('hpk', opcion, str(self.pesos_elementos[paso]))
				paso+=1

		f = open("./Datos/config.cfg", "w")  
		parser.write(f)
		f.close()  
		self.cargar_configuraciones()

	def vista_imagen(self,imagen):
		if self.configuracion=="HPK":
			cv2.rectangle(imagen, (114,81), (334,234), (255,0,0), 1) #terminal
			cv2.rectangle(imagen, (334,121), (450,204), (0,0,255), 1) #cable exterior
			cv2.rectangle(imagen, (223,121), (257,204), (0,255,0), 1) #sello rosenberger
			cv2.rectangle(imagen, (144,121), (223,204), (0,255,255), 1) #rosenberger
		else:
			cv2.rectangle(imagen, (114,81), (334,234), (255,0,0), 1) #terminal
			cv2.rectangle(imagen, (334,121), (499,204), (0,0,255), 1) #cable exterior
			cv2.rectangle(imagen, (203,121), (240,204), (0,255,0), 1) #candado
			cv2.rectangle(imagen, (164,121), (208,204), (0,255,255), 1) #anillo
		return imagen
		#cv2.imshow("cand", self.imagen)
		#time.sleep(3)

	def detector(self,imagen):
		self.entrada=[]
		if self.configuracion=="HPK":
			self.cinta_roja=self.detectar_componente(imagen,(self.rangos_minus['Cinta Roja'],self.rangos_mayus['Cinta Roja']),(121,334), (204,449)) #self.cinta_roja
			self.cinta_negra=self.detectar_componente(imagen,(self.rangos_minus['Cinta Negra'],self.rangos_mayus['Cinta Negra']),(121,334), (204,449))
			self.rosen_rojo=self.detectar_componente(imagen,(self.rangos_minus['Rosenberger Rojo'],self.rangos_mayus['Rosenberger Rojo']),(121,144), (204,223))
			self.sello=self.detectar_componente(imagen,(self.rangos_minus['Rosenberger Rojo'],self.rangos_mayus['Rosenberger Rojo']),(121,213), (204,257))
			self.entrada=np.array([[self.cinta_roja],[self.cinta_negra],[self.rosen_rojo],[self.sello]])
		else:
			self.cinta_roja=self.detectar_componente(imagen,(self.rangos_minus['Cinta Roja'],self.rangos_mayus['Cinta Roja']),(121,334), (204,499)) #self.cinta_roja=
			self.candado_rojo=self.detectar_componente(imagen,(self.rangos_minus['Candado Rojo'],self.rangos_mayus['Candado Rojo']),(121,203), (204,240)) #self.candado_rojo=
			self.candado_negro=self.detectar_componente(imagen,(self.rangos_minus['Candado Negro'],self.rangos_mayus['Candado Negro']),(121,203), (204,240)) #self.candado_negro=
			self.goma=self.detectar_componente(imagen,(self.rangos_minus['Goma'],self.rangos_mayus['Goma']),(121,334), (204,449))	 #self.goma=
			self.cover=self.detectar_componente(imagen,(self.rangos_minus['Cover'],self.rangos_mayus['Cover']),(121,334), (204,449)) #self.cover=
			self.anillo=self.detectar_componente(imagen,(self.rangos_minus['Candado Negro'],self.rangos_mayus['Candado Negro']),(121,164), (204,208)) #self.anillo=
			self.entrada=np.array([[self.cinta_roja],[self.candado_rojo],[self.candado_negro],[self.goma],[self.cover],[self.anillo]])
			
	def prueba(self,piezas_entrenamiento,elementos):
		os.system("clear") 
		self.cabecera()
		iteraciones=input("Numero de iteraciones: \nRespuesta:\t")
		os.system("clear") 
		self.cabecera()
		for i in range(iteraciones):
			self.autosalidas,entrada=[],[]
			harness=random.randint(0,10)
			print piezas_entrenamiento[harness][0][0]
			self.cargar_imagen(piezas_entrenamiento[harness][0][0],500.0)
			self.detector()
			for ii in range(elementos):
				self.salida=piezas_entrenamiento[harness][1][0][ii]
				self.autosalida=float(self.entrada[ii][0])/float(self.pesos_elementos[ii])
				if ii==5:
					if self.autosalida<0.7:
						self.autosalida=0.0
				self.autosalidas.append(round(self.autosalida))
			for i in range(len(self.autosalidas)):
				if i<3:
					entrada.append(self.autosalidas[i])
			self.neurona(entrada)
			print "____________________________"

	def produccion(self,imagen,elementos):
		self.detector(imagen)
		self.autosalidas,entrada=[],[]
		for ii in range(elementos):
			self.autosalida=float(self.entrada[ii][0])/float(self.pesos_elementos[ii])
			if ii==5:
				if self.autosalida<0.5:
					self.autosalida=0.0
			self.autosalidas.append(self.autosalida)
		for i in range(len(self.autosalidas)):
			if i<3:
				entrada.append(self.autosalidas[i])
		return entrada

	def configuraciones_setup(self):
		parser = SafeConfigParser()
		parser.read('./Datos/config.cfg')

		parser.set('general', 'cable', self.configuracion)

		cadena=["Cable","Cinta Roja","Cinta Negra","Rosenberger Rojo","Candado Rojo","Candado Negro","Cover","Goma"]
		cuenta_cadena,paso,paso_menor,conteo=0,0,0,0
		for opcion, valor in parser.items('rangos'):
			if paso==0:
				parser.set('rangos', opcion, str(self.rangos_minus[cadena[cuenta_cadena]][paso_menor]))
				paso_menor+=1
			if paso==1:
				parser.set('rangos', opcion, str(self.rangos_mayus[cadena[cuenta_cadena]][paso_menor]))
				conteo+=1
				paso_menor+=1
			if paso_menor==3:
				paso_menor=0
				paso+=1
			if conteo==3:
				cuenta_cadena+=1
				paso=0
				conteo=0

		f = open("./Datos/config.cfg", "w")  
		parser.write(f)
		f.close()  
		self.cargar_configuraciones()

	def configuraciones(self):
		os.system("clear") 
		self.cabecera()
		parser = SafeConfigParser()
		parser.read('./Datos/config.cfg')
		funcion=input("Opciones modificables: \n   -1=Cable \n   -2=***** \n   -3=***** \n   -4=***** \n   -5=***** \n   -6=**** \nRespuesta:\t")
		if funcion==1:
			os.system("clear") 
			self.cabecera()
			op=input("Tipos de cables: \n   -1=DCS \n   -2=HPK \nRespuesta:\t")
			if op==1:
				parser.set('general', 'cable', 'DCS')
			elif op==2:
				parser.set('general', 'cable', 'HPK')

		f = open("./Datos/config.cfg", "w")  
		parser.write(f)
		f.close()  
		self.cargar_configuraciones()
		