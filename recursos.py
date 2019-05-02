import pygame
import numpy as np

class text(object):
	def __init__(self,FontSize, FontName): 
		pygame.font.init()
		self.font=pygame.font.Font(FontName,FontSize)
		self.size=FontSize
	def render(self,surface,text,color,pos):
		text=unicode(text,"UTF-8")
		x,y=pos
		for i in text.split("\r"):
			text=surface.blit(self.font.render(i,1,color),(x,y))
			y += self.size
		return text

class cursor(pygame.Rect):
	def __init__(self): 
		pygame.Rect.__init__(self,0,0,1,1)
	def update(self):
		self.left,self.top=pygame.mouse.get_pos()

class toolbox(object):
	def __init__(self,fuente):
		self.fuente=fuente
	def updatefun(self,screen,message,xmss,ymss,xc,yc): 
		fontobject = pygame.font.Font(self.fuente,20)
		pygame.draw.rect(screen,recursos.BLACK,[xmss,ymss,xc,yc])
		#pygame.draw.rect(screen,recursos.BLACK,[0,529,1000,71])
		chtext.render(screen,message,recursos.GREEN,(xmss,ymss))
		chtext.render(screen,"Editando...  Salir con Enter",recursos.WHITE,(550,71))
		pygame.display.flip()
	def update(self,screen,message,xmss,ymss):
		fontobject = pygame.font.Font(self.fuente,20)
		chtext.render(screen,message,recursos.GREEN,(xmss,ymss))
	def fun(self,screen,xmss,ymss,xc,yc):
		pygame.font.init()
		current_string = []
		while 1:
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				inkey = event.key

				if inkey == K_BACKSPACE:
					current_string = current_string[0:-1]
				elif inkey == 13:
					break
				elif inkey == K_MINUS:
					current_string.append("-")
				elif (inkey>47 and inkey<58):
					current_string.append(chr(inkey))
			tb.updatefun(screen,string.join(current_string,""),xmss,ymss,xc,yc)
		try:
			return int(string.join(current_string,""))
		except:
			return 0
	def funstring(self,screen,xmss,ymss,xc,yc):
		pygame.font.init()
		current_string = []
		while 1:
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				inkey = event.key
				if inkey == K_BACKSPACE:
					current_string = current_string[0:-1]
				elif inkey == 13:
					break
				elif inkey == K_MINUS:
					current_string.append("-")
				elif inkey>47 and inkey<58 or inkey==46:
					current_string.append(chr(inkey))
			tb.updatefun(screen,string.join(current_string,""),xmss,ymss,xc,yc)
		if string.join(current_string,"")=="":
			return "0.0.0.0"
		else:
			return string.join(current_string,"")

class boton(object):	
	def __init__(self, img1,img2,h,l):
		self.imgn=img1
		self.imgs=img2
		self.imga=self.imgn
		self.rect=self.imga.get_rect()
		self.rect.left,self.rect.top=(h,l)

	def update(self,screen,cursor):
		if cursor.colliderect(self.rect):
			self.imga=self.imgs
		else: self.imga=self.imgn

		screen.blit(self.imga,self.rect)


piezas_entrenamiento_dcs=[
[["./Datos/Imagenes/dcs-1.jpg"],np.array([[0,0,1,1,1,0]])],
[["./Datos/Imagenes/dcs-2.jpg"],np.array([[0,0,1,1,1,0]])],
[["./Datos/Imagenes/dcs-3.jpg"],np.array([[0,0,0,1,1,0]])],
[["./Datos/Imagenes/dcs-4.jpg"],np.array([[1,1,0,1,1,1]])],
[["./Datos/Imagenes/dcs-5.jpg"],np.array([[1,1,0,1,1,1]])],
[["./Datos/Imagenes/dcs-6.jpg"],np.array([[1,0,0,1,1,0]])],
[["./Datos/Imagenes/dcs-7.jpg"],np.array([[1,0,0,1,1,0]])],
[["./Datos/Imagenes/dcs-8.jpg"],np.array([[1,0,0,1,1,0]])],
[["./Datos/Imagenes/dcs-9.jpg"],np.array([[1,1,0,1,1,0]])],
[["./Datos/Imagenes/dcs-10.jpg"],np.array([[1,1,0,1,1,0]])],
[["./Datos/Imagenes/dcs-11.jpg"],np.array([[0,0,0,1,1,0]])]]

piezas_entrenamiento_hpk=[
[["./Datos/Imagenes/hpk-1.jpg"],np.array([[1,0,1,1]])],
[["./Datos/Imagenes/hpk-2.jpg"],np.array([[1,0,1,1]])],
[["./Datos/Imagenes/hpk-3.jpg"],np.array([[1,0,1,1]])],
[["./Datos/Imagenes/hpk-4.jpg"],np.array([[0,1,0,1]])],
[["./Datos/Imagenes/hpk-5.jpg"],np.array([[0,1,0,1]])],
[["./Datos/Imagenes/hpk-6.jpg"],np.array([[0,1,0,1]])],
[["./Datos/Imagenes/hpk-7.jpg"],np.array([[0,1,0,0]])],
[["./Datos/Imagenes/hpk-8.jpg"],np.array([[0,1,0,0]])],
[["./Datos/Imagenes/hpk-9.jpg"],np.array([[0,1,0,0]])],
[["./Datos/Imagenes/hpk-10.jpg"],np.array([[0,1,0,0]])],
[["./Datos/Imagenes/hpk-11.jpg"],np.array([[1,0,1,0]])],
[["./Datos/Imagenes/hpk-12.jpg"],np.array([[1,0,1,0]])]]

rango_cable=[np.array((0,44,60)), np.array((39,196,255))]
rango_cinta_rojo=[np.array((0,0,75)), np.array((26,13,165))]
rango_cinta_negro=[np.array((0,0,0)), np.array((14,14,24))]
rango_rosenberger_rojo=[np.array((7,1,94)), np.array((77,55,255))]
rango_candado_rojo=[np.array((19,0,159)), np.array((85,63,210))]
rango_candado_negro=[np.array((20,20,20)), np.array((54,54,54))]
rango_cover=[np.array((0,0,0)), np.array((23,31,24))]
rango_goma=[np.array((0,75,65)), np.array((86,199,204))]


fuente3="./Datos/fuentes/Prototype.ttf"
fuente2="./Datos/fuentes/MontereyFLF-BoldItalic.ttf"
fuente1="./Datos/fuentes/DejaVuSerif.ttf"
fuente4="./Datos/fuentes/NanumMyeongjo.ttf"
fuente5="./Datos/fuentes/Sullivan.ttf"
#DejaVuSerif
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#DODGER_BLUE = (30, 144, 255)
DODGER_BLUE = (51, 156, 255)
STEEL_BLUE = (70, 130, 180)
RED=(255,0,0)
GREEN=(0,255,0)
other=(234,115,94)
GRAY=(150,150,150)
#######################################################Valores############################################################## 
xm=ym=fg=centx=centy=st=0.0
tg=1.0
xy_cor = [400,300]
centx=xy_cor[0]
centy=xy_cor[1]
tiempo_espera=2
###############################################botones##################################################
#uvlogo=pygame.image.load("./Datos/iconos/Logo-UV2.jpg")
uvlogo=pygame.image.load("./Datos/iconos/brain.png")
connect=pygame.image.load("./Datos/iconos/wifi-llena.png")
unconnect=pygame.image.load("./Datos/iconos/wifi-llena (1).png")
checkb=pygame.image.load("./Datos/iconos/bien.png")
checka=pygame.image.load("./Datos/iconos/bien(1).png")

guardara=pygame.image.load("./Datos/iconos/guardar.png")
guardarb=pygame.image.load("./Datos/iconos/guardar(1).png")

warningr=pygame.image.load("./Datos/iconos/mal(1).png")
cirmenosb=pygame.image.load("./Datos/iconos/circle.png")
cirmenosa=pygame.image.load("./Datos/iconos/circle (1).png")
cirmasb=pygame.image.load("./Datos/iconos/technology.png")
cirmasa=pygame.image.load("./Datos/iconos/technology (1).png")
fondoneg=pygame.image.load("./Datos/iconos/fondoneg.jpg")
gris=pygame.image.load("./Datos/iconos/color_gris.jpg")

textura=pygame.image.load("./Datos/iconos/fondo.jpg")

success=pygame.image.load("./Datos/iconos/success.png")
error=pygame.image.load("./Datos/iconos/error.png")
success=pygame.transform.scale(success, (64,64))
error=pygame.transform.scale(error, (64,64))

b_success=boton(success,success,1000,475)
b_error=boton(error,error,1100,475)
#buv=load_image("./Datos/iconos/ojo_negro.jpg",True)
#buv=boton(uvlogo,uvlogo,450,125)
#buv=boton(uvlogo,uvlogo,200,75)
bcone=boton(connect,connect,1132,2)
bucone=boton(unconnect,unconnect,1132,2)

b_mas_1=boton(cirmasb,cirmasa,577,445) #R-
b_menos_1=boton(cirmenosb,cirmenosa,552,445)

b_mas_2=boton(cirmasb,cirmasa,1130,445) #R+
b_menos_2=boton(cirmenosb,cirmenosa,1105,445)

b_mas_3=boton(cirmasb,cirmasa,577,470) #G-
b_menos_3=boton(cirmenosb,cirmenosa,552,470)

b_mas_4=boton(cirmasb,cirmasa,1130,470) #G+
b_menos_4=boton(cirmenosb,cirmenosa,1105,470)

b_mas_5=boton(cirmasb,cirmasa,577,495) #B-
b_menos_5=boton(cirmenosb,cirmenosa,552,495)

b_mas_6=boton(cirmasb,cirmasa,1130,495) #B+
b_menos_6=boton(cirmenosb,cirmenosa,1105,495)

bwarncoor=boton(warningr,warningr,1130,430)
bacepbz=boton(checkb,checka,1130,430)
#bacepcf=boton(checkb,checka,1130,430)
bacepbzfin=boton(checkb,checka,1030,100)

b_guardar=boton(guardara,guardarb,1130,530)