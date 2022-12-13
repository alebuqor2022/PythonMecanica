import tkinter
import pyfirmata
from time import sleep
from tkinter import *
from tkinter import ttk
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from tkinter.messagebox import showinfo
from tkinter import messagebox

localhost = "127.0.0.1"
puerto = 3306
usernameDB = "root"
passw = "1234"
db = "ventilador"
options = {'fill': 'both', 'padx': 10, 'pady': 10, 'ipadx': 5}
logueado = False
def main():
	#Funcion de boton login
	def onLogin():
		global logueado
		username = usuario.get()
		passwordU = contra.get()
		connection = pymysql.connect(host=localhost,port=puerto,user=usernameDB,password = passw,database = db)
		cursor = connection.cursor()
		cursor.execute("SELECT password FROM login WHERE usuario='{}'".format(username))
		result = cursor.fetchone()
		try:
			if(check_password_hash(result[0],passwordU)):
				messagebox.showinfo(title='Information',message='Logueo satisfactorio')
				logueado = True
				login.destroy()
			else:
				messagebox.showinfo(title='Login',message='Contraseña o usuario incorrectos')
		except:
				messagebox.showinfo(title='Login',message='Contraseña o usuario incorrectos')
		cursor.close
		connection.close
	#Funcion de boton register
	def onRegister():
		global logueado
		username = usuario.get()
		username = username.replace(" ", "")
		passwordU = generate_password_hash(contra.get(),'sha256',50)
		connection = pymysql.connect(host=localhost,port=puerto,user=usernameDB,password = passw,database = db)
		cursor = connection.cursor()
		try:
			cursor.execute("INSERT into login (usuario, password) values ('{}', '{}')".format(username,passwordU))
			connection.commit()
			messagebox.showinfo(title='Information',message='Registro satisfactorio')
			login.destroy()
			logueado = True
		except:
			connection.rollback()
			
			messagebox.showinfo(title='Information',message='El nombre de usuario ya existe o no se pudo crear el usuario')
		cursor.close
		connection.close
  
    #Creamos la ventana de inicio de sesion
	login = tkinter.Tk()
	login.title("Inicio de sesion")
	
	#Background
	login.config(bg="black")

	#Ingreso de variables
 
	#usuario
	Label(login, text="Usuario",bg="black",foreground = "white").grid(row=0, column=0)
	usuario = tkinter.StringVar()
	tkinter.Entry(textvariable = usuario).grid(row=0, column=1)
 
	#contraseña
	Label(login,text="Contraseña",bg="black",foreground = "white").grid(row=1, column=0)
	contra = tkinter.StringVar()
	tkinter.Entry(textvariable=contra, show='*').grid(row=1, column=1)
	
	#botones
	tkinter.Button(login,text="login",width=15,bg="white",command=onLogin).grid(row=2, column=1)
	tkinter.Button(login,text="register",width=15,bg="white",command=onRegister).grid(row=3, column=1)
	

	#Inicio la pantalla de inicio de sesion
	login.mainloop()
	
	if logueado == True:

		#Creamos la ventana de regulacion del ventilador
		top = tkinter.Tk()
		top.title("Control de Ventilador")

		#Color de fondo
		top.config(bg="black") 
		
		#Funcion de boton iniciar
		def onStartButtonPress():
			#Restardo a obtener desde la gui
			timePeriod = timePeriodEntry.get()
			timePeriod = float(timePeriod)
			ledBrightness = brightnessScale.get()
			ledBrightness = float(ledBrightness)
			port = comEntry.get()
			board = pyfirmata.Arduino(port)
			ledPin = board.get_pin('d:3:p')
			startButton.config(state=tkinter.DISABLED)
			ledPin.write(ledBrightness/100.0)
			sleep(timePeriod)
			ledPin.write(0)
			startButton.config(state=tkinter.ACTIVE)
			board.exit()


		#Slide Tiempo	
		timePeriodEntry = tkinter.Scale(top,length=200,sliderlength=30,width=15,bg="black",troughcolor="gray",foreground = "white",from_=0, to=60,orient=tkinter.HORIZONTAL)
		timePeriodEntry.grid(column=1, row=2)
		tkinter.Label(top, text="Tempo en seg",bg="#666666",fg="white").grid(column=1, row=0)

		#Slide Velocidad
		brightnessScale = tkinter.Scale(top,length=200,sliderlength=30,width=15,bg="black",troughcolor="gray",fg="white",from_=0, to=100,orient=tkinter.HORIZONTAL)
		brightnessScale.grid(column=1, row=5),
		tkinter.Label(top, text="Velocidad %",bg="#666666",fg="white").grid(column=1, row=4)
		comEntry = tkinter.Entry(top)
		comEntry.grid(column=0, row=2)
		tkinter.Label(top, text="Escribe el Puerto COM",bg="#666666",fg="white").grid(column=0, row=0)

		#Bonton Iniciar
		startButton = tkinter.Button(top,text="Iniciar",width=15,bg="white",command=onStartButtonPress)
		startButton.grid(column=0, row=4)

		#Boton Exit
		exitButton = tkinter.Button(top,text="Salir",width=15,bg="white",command=top.quit)

		exitButton.grid(column=0, row=5)
			
			
		brightnessScale.grid()
		timePeriodEntry.grid()
		startButton.grid()
		top.mainloop()
	else: print('Debe loguearse para poder acceder al ventilador')
main()
