#!/usr/bin/env python
import time,math,pygame,string,socket,os,threading,numpy,cv2
import recursos,isabel
from pygame.locals import *
from ConfigParser import SafeConfigParser
global running
running=True

class interfaz(object):
	def __init__(self):
		pygame.init()
		self.captura,self.tiempo_apren,self.autonomia,self.tiempo,self.screen = 0,0,0,0,pygame.display.set_mode((1200,600)) 	
		self.estado,self.vista,self.marcos="Produccion","Normal",0
		self.nombre,self.version,self.empresa="Isabel","v.0.90.0","Yazaki North America"
		self.botones_menu={"Produccion":[0,(15,50)],"Aprendizaje":[0,(15,80)],"Configuracion":[0,(15,110)],"Ayuda":[0,(15,140)]}
		self.botones_prueba={}
		self.botones_apren={"Manual":[0,(250,50)],"Autonomo":[0,(250,80)],"Captura":[0,(250,150)]}
		self.botones_config={"Cable:":[0,(250,50)]}
		self.botones_prod={"Captura":[0,(250,400)],"Marcos":[0,(250,375)]}
		self.camara=cv2.VideoCapture(0);
		self.FontName="./Datos/fuentes/NanumMyeongjo.ttf"
		self.cargar_configuraciones()

	def main_controles(self):
		global running
		print ("[Controles]: Programa iniciado")
		while running: 	
			mouse.update()								 
			for event in pygame.event.get():
				if event.type == QUIT:
					running=False
					cv2.destroyAllWindows()
				try:
					print(self.estado)
					try:
						if self.estado=="Produccion" or self.estado=="Aprendizaje":
							if event.key == pygame.K_SPACE:
								self.mensajes=[]
								if isabelv.configuracion=="DCS":
									self.mensajes=isabelv.neurona(isabelv.produccion(self.imagen,6))
								else:
									self.mensajes=isabelv.neurona(isabelv.produccion(self.imagen,4))
								self.captura=1
					except:
						print("Error")
						pass

					print("rr")
					if event.type == pygame.MOUSEBUTTONDOWN:
						print("ff")
						for leyenda in self.botones_menu:
							if mouse.colliderect(self.botones_menu[leyenda][0]):
								self.estado=leyenda
						if self.estado=="Produccion":
							for leyenda in self.botones_vista:
								if mouse.colliderect(self.botones_vista[leyenda][0]):
									self.vista=leyenda
							if mouse.colliderect(self.botones_prod["Captura"][0]):
								self.mensajes=[]
								if isabelv.configuracion=="DCS":
									self.mensajes=isabelv.neurona(isabelv.produccion(self.imagen,6))
								else:
									self.mensajes=isabelv.neurona(isabelv.produccion(self.imagen,4))
								self.captura=1
							if mouse.colliderect(self.botones_prod["Marcos"][0]):
								if self.marcos==0:
									self.marcos=1
								else: 
									self.marcos=0
						if self.estado=="Configuracion":
							for leyenda in self.botones_vista:
								if mouse.colliderect(self.botones_vista[leyenda][0]):
									self.vista=leyenda
							if mouse.colliderect(self.botones_config["Cable:"][0]):
								if isabelv.configuracion=='DCS':
									isabelv.configuracion='HPK'
								else:
									isabelv.configuracion='DCS'
							if mouse.colliderect(recursos.b_guardar.rect):
								isabelv.rangos_minus=self.rangos_minus
								isabelv.rangos_mayus=self.rangos_mayus
								isabelv.configuraciones_setup()
								self.cargar_configuraciones()
								print ("[Setup]: Configuraciones guardadas")

							if mouse.colliderect(recursos.b_mas_1.rect):
								self.rangos_minus[self.vistas[self.vista]][2]+=2
							if mouse.colliderect(recursos.b_mas_2.rect):
								self.rangos_mayus[self.vistas[self.vista]][2]+=2
							if mouse.colliderect(recursos.b_mas_3.rect):
								self.rangos_minus[self.vistas[self.vista]][1]+=2
							if mouse.colliderect(recursos.b_mas_4.rect):
								self.rangos_mayus[self.vistas[self.vista]][1]+=2
							if mouse.colliderect(recursos.b_mas_5.rect):
								self.rangos_minus[self.vistas[self.vista]][0]+=2
							if mouse.colliderect(recursos.b_mas_6.rect):
								self.rangos_mayus[self.vistas[self.vista]][0]+=2

							if mouse.colliderect(recursos.b_menos_1.rect):
								self.rangos_minus[self.vistas[self.vista]][2]-=2
							if mouse.colliderect(recursos.b_menos_2.rect):
								self.rangos_mayus[self.vistas[self.vista]][2]-=2
							if mouse.colliderect(recursos.b_menos_3.rect):
								self.rangos_minus[self.vistas[self.vista]][1]-=2
							if mouse.colliderect(recursos.b_menos_4.rect):
								self.rangos_mayus[self.vistas[self.vista]][1]-=2
							if mouse.colliderect(recursos.b_menos_5.rect):
								self.rangos_minus[self.vistas[self.vista]][0]-=2
							if mouse.colliderect(recursos.b_menos_6.rect):
								self.rangos_mayus[self.vistas[self.vista]][0]-=2
						if self.estado=="Aprendizaje":
							if mouse.colliderect(self.botones_apren["Captura"][0]):
								self.mensajes=[]
								self.mensajes=isabelv.neurona(isabelv.produccion(self.imagen,6))
								self.captura=1
							if self.autonomia==1:
								pass
							else:
								if mouse.colliderect(recursos.b_success.rect):
									self.mensajes.append(isabelv.entrenamiento_manual())
									self.tiempo_apren=1
								if mouse.colliderect(recursos.b_error.rect):
									self.mensajes.append(isabelv.entrenamiento_manual(True))
									self.tiempo_apren=1
							if mouse.colliderect(self.botones_apren["Manual"][0]):
								self.autonomia=0
							if mouse.colliderect(self.botones_apren["Autonomo"][0]):
								self.autonomia=1
				except:
					print("[Controles]: Error")
					pass
		print ("[Controles]: Programa finalizado")

	def cargar_configuraciones(self):
		self.rangos_minus=isabelv.rangos_minus
		self.rangos_mayus=isabelv.rangos_mayus
		#print 2,self.rangos_minus
		if isabelv.configuracion=="DCS":
			self.vistas={"Normal":0,"Cinta Roja":"Cinta Roja","Candado Rojo":"Candado Rojo","Candado Negro":"Candado Negro","Goma":"Goma","Cover":"Cover","Anillo":"Candado Negro"}
			self.botones_vista={"Normal":[0,(270,140)],"Cinta Roja":[0,(270,170)],"Candado Rojo":[0,(270,200)],"Candado Negro":[0,(270,230)],"Goma":[0,(270,260)],"Cover":[0,(270,290)],"Anillo":[0,(270,320)]}
		else:
			self.vistas={"Normal":0,"Cinta Roja":"Cinta Roja","Cinta Negra":"Cinta Negra","Rosenberger Rojo":"Rosenberger Rojo","Sello":"Rosenberger Rojo"}
			self.botones_vista={"Normal":[0,(270,140)],"Cinta Roja":[0,(270,170)],"Cinta Negra":[0,(270,200)],"Rosenberger Rojo":[0,(270,230)],"Sello":[0,(270,260)]}

	def mostrar_botones(self,botones):
		for leyenda in botones:
			botones[leyenda][0]=chtext.render(self.screen,leyenda,recursos.DODGER_BLUE,botones[leyenda][1])
			if self.vista==leyenda:
				chtext.render(self.screen,leyenda,recursos.GREEN,botones[leyenda][1])
			if self.estado==leyenda:
				chtext.render(self.screen,leyenda,recursos.GREEN,botones[leyenda][1])
			if mouse.colliderect(botones[leyenda][0]):
				if botones==self.botones_menu:
					pygame.draw.line(self.screen, recursos.GREEN,(botones[leyenda][1][0],botones[leyenda][1][1]+20), (200,botones[leyenda][1][1]+20),2)
				else:
					pygame.draw.line(self.screen, recursos.GREEN,(botones[leyenda][1][0]+botones[leyenda][0][2],botones[leyenda][1][1]+20), (200,botones[leyenda][1][1]+20),2)

	def cabecera(self):
		self.screen.fill((0,0,0))
		self.screen.blit(recursos.uvlogo,(344,44))								
		ltext.render(self.screen,"Interfaz de control para "+self.nombre+" - "+self.version,recursos.WHITE,(260,0))
		ltext.render(self.screen,self.empresa,recursos.WHITE,(10,550))
		pygame.display.flip()
		time.sleep(0.5)

	def grid(self,screen):
		y=0 
		for i in range(12):
			x=0
			for ii in range(26):
				xchtext.render(screen,"("+str(x)+","+str(y)+")",recursos.WHITE,(x,y))
				x+=50
			y+=50

		y=50
		for i in range(12):
			pygame.draw.line(screen, recursos.WHITE, (0,y), (1200,y),1)
			y+=50

		x=50
		for i in range(26):
			pygame.draw.line(screen, recursos.WHITE, (x,0), (x,600),1)
			x+=50

	def produccion(self):
		self.mostrar_botones(self.botones_vista)
		self.mostrar_botones(self.botones_prod)
		self.cargar_imagen(500.0)
		chtext.render(self.screen,"Vista",recursos.WHITE,(250,100))

		#self.j=self.text_render("Jairo",recursos.WHITE,(450,200),40)
		if self.captura==1:
			self.tiempo+=1
			paso=450
			for aviso in self.mensajes:
				if aviso=="Harness correcto":
					chtext.render(self.screen,aviso,recursos.GREEN,(250,paso))
				else:
					chtext.render(self.screen,aviso,recursos.RED,(250,paso))
				paso+=30 
			if self.tiempo==70:
				self.tiempo,self.captura=0,0

		if self.marcos==1:
			self.imagen=isabelv.vista_imagen(self.imagen)
			chtext.render(self.screen,'Marcos',recursos.GREEN,self.botones_prod['Marcos'][1])
			#pygame.draw.line(self.screen, recursos.GREEN,(self.botones_prod['Marcos'][1][0]+self.botones_prod['Marcos'][0][2],self.botones_prod['Marcos'][1][1]+20), (200,self.botones_prod['Marcos'][1][1]+20),2)
		
		self.imagen_pygame = numpy.rot90(self.imagen)
		for leyenda in self.botones_vista:
			if self.vista=="Normal":
				self.imagen_pygame = cv2.cvtColor(self.imagen_pygame, cv2.COLOR_BGR2RGB)
				self.imagen_pygame = pygame.surfarray.make_surface(self.imagen_pygame)
				break
			elif self.vista==leyenda:
				self.imagen_pygame = pygame.surfarray.make_surface(cv2.inRange(self.imagen_pygame,self.rangos_minus[self.vistas[leyenda]],self.rangos_mayus[self.vistas[leyenda]]))
				break
		self.screen.blit(self.imagen_pygame, (600,50))

	def aprendizaje(self):
		self.captura=0
		self.mostrar_botones(self.botones_apren)
		self.cargar_imagen(500.0)
		if self.captura==1:
			if self.tiempo_apren==0:
				recursos.b_success.update(self.screen,mouse)
				recursos.b_error.update(self.screen,mouse)
			paso=450
			for aviso in self.mensajes:
				if aviso=="Harness correcto":
					chtext.render(self.screen,aviso,recursos.GREEN,(250,paso))
				else:
					chtext.render(self.screen,aviso,recursos.RED,(250,paso))
				paso+=30 

			if self.tiempo_apren==1:
				self.tiempo+=1
			if self.tiempo==70:
				self.tiempo_apren,self.captura,self.tiempo=0,0,0

		if self.autonomia==1:
			chtext.render(self.screen,"Autonomo",recursos.GREEN,self.botones_apren["Autonomo"][1])
		else:
			chtext.render(self.screen,"Manual",recursos.GREEN,self.botones_apren["Manual"][1])

		

		self.imagen_pygame = numpy.rot90(self.imagen)
		self.imagen_pygame = cv2.cvtColor(self.imagen_pygame, cv2.COLOR_BGR2RGB)
		self.imagen_pygame = pygame.surfarray.make_surface(self.imagen_pygame)
		self.screen.blit(self.imagen_pygame, (600,50))

	def configuracion(self):
		self.captura=0
		rgbm=["R-","G-","B-"]
		rgbmm=["R+","G+","B+"]
		self.mostrar_botones(self.botones_vista)
		self.mostrar_botones(self.botones_config)
		self.cargar_imagen(500.0)
		chtext.render(self.screen,"Vista",recursos.WHITE,(250,100))
		chtext.render(self.screen,str(isabelv.configuracion),recursos.WHITE,(320,50))
		recursos.b_guardar.update(self.screen,mouse)

		recursos.b_mas_1.update(self.screen,mouse)
		recursos.b_mas_2.update(self.screen,mouse)
		recursos.b_mas_3.update(self.screen,mouse)
		recursos.b_mas_4.update(self.screen,mouse)
		recursos.b_mas_5.update(self.screen,mouse)
		recursos.b_mas_6.update(self.screen,mouse)

		recursos.b_menos_1.update(self.screen,mouse)
		recursos.b_menos_2.update(self.screen,mouse)
		recursos.b_menos_3.update(self.screen,mouse)
		recursos.b_menos_4.update(self.screen,mouse)
		recursos.b_menos_5.update(self.screen,mouse)
		recursos.b_menos_6.update(self.screen,mouse)

		paso,paso_2=440,450
		for i in range(len(rgbm)):
			chtext.render(self.screen,rgbm[i],recursos.WHITE,(527,paso))
			chtext.render(self.screen,rgbmm[i],recursos.WHITE,(1160,paso))
			pygame.draw.line(self.screen, recursos.GRAY, (600,paso_2), (1100,paso_2),2)
			paso+=25
			paso_2+=25

		self.imagen_pygame = numpy.rot90(self.imagen)
		for leyenda in self.botones_vista:
			if self.vista=="Normal":
				self.imagen_pygame = cv2.cvtColor(self.imagen_pygame, cv2.COLOR_BGR2RGB)
				self.imagen_pygame = pygame.surfarray.make_surface(self.imagen_pygame)
				break
			elif self.vista==leyenda:
				self.imagen_pygame = pygame.surfarray.make_surface(cv2.inRange(self.imagen_pygame,self.rangos_minus[self.vistas[leyenda]],self.rangos_mayus[self.vistas[leyenda]]))
				chtext.render(self.screen,str(self.rangos_minus[self.vistas[leyenda]][2]),recursos.RED,(600+(self.rangos_minus[self.vistas[leyenda]][2]*2),440))
				chtext.render(self.screen,str(self.rangos_mayus[self.vistas[leyenda]][2]),recursos.RED,(590+(self.rangos_mayus[self.vistas[leyenda]][2]*2),440))
				chtext.render(self.screen,str(self.rangos_minus[self.vistas[leyenda]][1]),recursos.GREEN,(605+(self.rangos_minus[self.vistas[leyenda]][1]*2),465))
				chtext.render(self.screen,str(self.rangos_mayus[self.vistas[leyenda]][1]),recursos.GREEN,(590+(self.rangos_mayus[self.vistas[leyenda]][1]*2),465))
				chtext.render(self.screen,str(self.rangos_minus[self.vistas[leyenda]][0]),recursos.DODGER_BLUE,(605+(self.rangos_minus[self.vistas[leyenda]][0]*2),490))
				chtext.render(self.screen,str(self.rangos_mayus[self.vistas[leyenda]][0]),recursos.DODGER_BLUE,(590+(self.rangos_mayus[self.vistas[leyenda]][0]*2),490))
				break
		try:
			self.screen.blit(self.imagen_pygame, (600,50))
		except:
			self.vista="Normal"

	def cargar_imagen(self,factor_dimension):
		ret, self.imagen = self.camara.read()
		dim = (int(factor_dimension), int(self.imagen.shape[0] * (factor_dimension / self.imagen.shape[1])))
		self.imagen = cv2.resize(self.imagen, dim, interpolation = cv2.INTER_AREA)

	def cargar_imagen2(self,direccion,factor_dimension):
		self.imagen=cv2.imread(direccion)
		dim = (int(factor_dimension), int(self.imagen.shape[0] * (factor_dimension / self.imagen.shape[1])))
		self.imagen = cv2.resize(self.imagen, dim, interpolation = cv2.INTER_AREA)

	def main(self):	
		global running
		pygame.display.set_caption("Interfaz de control para "+self.nombre+" - "+self.version)
		controles=threading.Thread(target=self.main_controles) 				
		controles.start()
		self.cabecera()
		try:
			while running: 	
				for event in pygame.event.get():
					if event.type == QUIT:
						running=False
						cv2.destroyAllWindows()

				self.screen.fill((50,50,50))
				self.screen.blit(recursos.textura,(0,0))
				#self.grid(self.screen)
				#pygame.draw.line(self.screen, recursos.WHITE, (200,25), (200,575),2)
				self.mostrar_botones(self.botones_menu)

				xchtext.render(self.screen,"Cable: "+isabelv.configuracion,recursos.WHITE,(15,500))
				xchtext.render(self.screen,"Ciclos: "+str(isabelv.ciclos),recursos.WHITE,(15,520))
				xchtext.render(self.screen,"Ing. Jairo Lara",recursos.WHITE,(15,540))
				xchtext.render(self.screen,"Yazaki North America",recursos.WHITE,(15,560))

				if self.estado=="Produccion":
					self.produccion()
				elif self.estado=="Aprendizaje":
					self.aprendizaje()
				elif self.estado=="Configuracion":
					self.configuracion()

				pygame.display.flip()
		except:
			running=False
			print ("[Setup]: Error en la interfaz")

		self.cabecera()
		pygame.quit()

if __name__ == '__main__':
	print ("[Setup]: Programa iniciado")
	isabelv=isabel.vision()

	interface=interfaz()
	fuente_general=recursos.fuente1
	ltext=recursos.text(40,fuente_general)
	chtext=recursos.text(20,fuente_general)
	xchtext=recursos.text(15,fuente_general)
	mouse=recursos.cursor()

	tb=recursos.toolbox(fuente_general)
	interface.main()
	print ("[Setup]: Programa terminado")
	