#!/usr/bin/env python
#El comentario que esta en la primera linea siempre hay que ponerlo para que funcione el Script de Python.


#IMPORTAMOS LIBRERIAS
#1-Importamos las librerias que usamos a lo largo del Script.
#0-Para ello previeamente han de haber sido descargadas e instaladas en el dispositivo en el que vamos
#a correr este Script en mi caso en la Raspi.
import RPi.GPIO as GPIO
from gpiozero import OutputDevice
import mysql.connector
from mysql.connector import Error
import time


################DECLARACIONES##############################################################
#Declaramos las LEDS que vamos a utilizar.
LED1=14
LED2=15
LED3=18
LED4=23

#Declaramos el ventilador que vamos a utilizar.
CONTROLVENTI=24

#Declaramos las variables de conexion de ambito global.
queryConsulta=""
queryActualizar=""

#Declaramos variable del codigo del invernadero.
id_invernadero="12345678"

#Declaramos variables que nos haran falta a lo largo del Script.
queryUsuario=""
record=[]

###########################################################################################


#FUNCION CONEXION
#1-Nos conectamos a nuestra BBDD de AWS, al tener la BBDD una IP elactica nunca cambia por lo que
#va a ser siempre la misma, ponemos el puerto por el que esta MySql, la BBDD que estamos utilizando
#y las claves para poder entrar.
try:
    connection = mysql.connector.connect(host='3.14.208.112', port='3306',database='invernadero02',user='root',password= '1122')
    print("Se ha realizado la conexion a la bbdd")
        
except Error as e:
    print("Error while connecting to MySQL", e)


#FUNCION CERRAR CONEXION
def cerrarConexion():
    try:
        connection.close()
        print("Se ha cerrado la conexion a la bbdd")

    except Error as e:
        print("Error while connecting to MySQL", e)


#FUNCION ENCENDER LED
def encenderLed():
    print("vamos a encender las luces")
    GPIO.output(LED1, GPIO.HIGH)
    GPIO.output(LED2, GPIO.HIGH)
    GPIO.output(LED3, GPIO.HIGH)
    GPIO.output(LED4, GPIO.HIGH)


#FUNCION APAGAR LED
def apagarLed():
    print("vamos a apagar las luces")
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)


#FUNCION ENCENDER VENTILADOR
def encenderVentilador():
    print("vamos a encender el ventilador")
    GPIO.output(CONTROLVENTI, True)


#FUNCION APAGAR VENTILADOR
def apagarVentilador():
    print("vamos a apagar el ventilador")
    GPIO.output(CONTROLVENTI, False)


#TODAS LAS CONSULTAS/UPDATES QUE HACEMOS A LA BBDD
#1-Comprobamos si la conexión se ha abierto correctamente y en caso de ser asi ejecutara la query que nos entra por parametro.
#2-Tenemos una comrpbación por si recibimos un "NULL" (Esto puede pasar caundo no encuentra a ningun asuario asiganado a este
#invernadero).
#3-Si no recibimos un "NULL" devolvemos el primer campo que nos devuelve la consulta, en este caso es siempre el que queremos ya que
#en las querys lo indicamos en vez de poner un (*).
def consultaBbdd(query):
    print("Vamos a hacer consulta a la bbdd")
    try:
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute(query)
            record= cursor.fetchone()

            if record != None:
                return record[0]
            else:
                return "Oka"
    except Error as e:
        print("Error consultabbdd", e)
    print("hemos terminado la consulta a la bbdd")


#FUNCION GLOBAL DE LAS LEDS
#1-Empezamos inicializando las LEDS a tipo OUT.
#2-Buscamos si la planta que nos pasan por parametro necesita que se ilumine, eso lo haremos con la "queryConsulta"
#en caso de recibir un 1 hace falta que se ilumine y en caso de recibir un 0 es que no hace falta que se ilumine.
#3-Llmamos a la funcion "consultaBbdd()" a la cual la pasamos por parametro la "queryConsulta", esta funcion hace una consulta
#a nuestra BBDD y el resultado que obtenga (1 o 0) se almacenara en la variable resultado.
#4-Lo siguiente que se comprobara es si ese resultado es como indicabamos (1 o 0) en caso de que sea 1:
#4.1-Llamaremos a la funcion "encenderLed()" la cual hara que se enciendan las leds.
#4.2-Despues esperara 10s.
#4.3-A continuacion se llamara a la funcion "apagarLed()" la cual hara que se apagen las leds.
#4.4-Y a continuacion se tendra que actualizar la BBDD el campo "querer_luz" a "0" para indicar que ya no hace falta
#que se ilumine por que se acaba de iluminar hace 10s.
#4.5-Se crea una nueva query "queryActualizar" que en vez de un "select" es un "update" y se vuelve a llamar a la funcion "consultaBbdd()".
#5-Y ya habria terminado el proceso global de LEDS.
def procesoLed(id_planta):
    print("empezamos el proceso de las LED")
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)
    GPIO.setup(LED4, GPIO.OUT)

    queryConsulta = "select querer_luz from personalizarplanta where id_planta="+ str(id_planta)
    print(queryConsulta)

    resultado = consultaBbdd(queryConsulta)
    
    if resultado == 1:
        encenderLed()
        time.sleep(10)
        apagarLed()
        queryActualizar ="update personalizarplanta set querer_luz = 0 where id_planta ="+ str(id_planta)
        print(queryActualizar)
        respuesta =consultaBbdd(queryActualizar)
        print("se ha modificado el valor a ", str(respuesta), " de las leds")

    print("terminamos el proceso de las LED")


#FUNCION GLOBAL DEL VENTILADOR
#1-Empezamos inicializando el Ventilador a tipo OUT.
#2-Buscamos si la planta que nos pasan por parametro necesita que se ventile, eso lo haremos con la "queryConsulta"
#en caso de recibir un 1 hace falta que se ventile y en caso de recibir un 0 es que no hace falta que se ventile.
#3-Llmamos a la funcion "consultaBbdd()" a la cual la pasamos por parametro la "queryConsulta", esta funcion hace una consulta
#a nuestra BBDD y el resultado que obtenga (1 o 0) se almacenara en la variable resultado.
#4-Lo siguiente que se comprobara es si ese resultado es como indicabamos (1 o 0) en caso de que sea 1:
#4.1-Llamaremos a la funcion "encenderVentilador()" la cual hara que se encienda el ventilador.
#4.2-Despues esperara 10s.
#4.3-A continuacion se llamara a la funcion "apagarVentilador()" la cual hara que se apage el ventilador.
#4.4-Y a continuacion se tendra que actualizar la BBDD el campo "querer_ventilar" a "0" para indicar que ya no hace falta
#que se ventile por que se acaba de ventilar hace 10s.
#4.5-Se crea una nueva query "queryActualizar" que en vez de un "select" es un "update" y se vuelve a llamar a la funcion "consultaBbdd()".
#5-Y ya habria terminado el proceso global del Ventilador.
def procesoVentilador(id_planta):
    print("empezamos el proceso del ventilador")
    GPIO.setup(CONTROLVENTI, GPIO.OUT)

    queryConsulta = "select querer_ventilar from personalizarplanta where id_planta="+ str(id_planta)
    print(queryConsulta)

    resultado = consultaBbdd(queryConsulta)

    if resultado == 1:
        encenderVentilador()
        time.sleep(10)
        apagarVentilador()
        queryActualizar ="update personalizarplanta set querer_ventilar = 0 where id_planta =" + str(id_planta)
        print(queryActualizar)
        respuesta =consultaBbdd(queryActualizar)
        print("se ha modificado el valor a", str(respuesta), "del ventilador")

    print("terminamos el proceso del ventilador")


#FUNCION RECOGER LA PLANTA DEL INVERNADERO DEL USUARIO VINCULADO AL INVERNADERO
#1-A esta funcion se la pasa el usuario con el que esta vinculado este invernadero(por el id_invernadero).
#2-Lo que haremos sera hacer una consulta a la BBDD para saber que planta es la que esta asociada al invernadero, tambien
#hay que tener en cuenta que el usuario puede tener mas de una planta pero SOLO UNA en el invernadero y solo esta cuidando a una
#por lo que en la "queryPlanta" se comprueba tambien la "fecha_fin" ya que si la "fecha_fin" es "NULL" quiere decir que no tiene fecha,
#esto indica que es la planta actual que esta en el invernadero ahora mismo.
#3-Llamaremos a la funcion "consultaBbdd()" para saber el ID de la planta con el que vamos a trabajar.
def recogerPlanta(usuario):
    queryPlanta= "SELECT * FROM personalizarplanta WHERE id_usuario="+ str(usuario)+" and fecha_fin IS NULL"
    print(queryPlanta)
    respuesta =consultaBbdd(queryPlanta)
    return respuesta


#FUNCION RECOGE EL USUARIO QUE ESTA ASOCIADO A ESTE INVERNADERO
#1-Hacemos una consulta a la BBDD con la funcion "consultaBbdd()" para saber y recoger que usuario esta
#asociado al invernadero (id_invernadero --> esta definido arriba del todo).
def recogerUsuario():
    print("Pillamos usuario")
    queryUsuario= "SELECT id_usuario from usuario where codigo_invernadero ="+ str(id_invernadero)
    print(queryUsuario)
    #la respuesta es el id_usuario
    respuesta = consultaBbdd(queryUsuario)
    return respuesta


#FUNCIONAMIENTO DEL SCRIPT
#1-Va a ser un bucle constante.
#2-Declaramos como va a estar conectado el circuito electronico a la Raspi.
#3-Almacenamos en "usuario" el usuario que esta asociado a este invernadero --> "recogerUsuario()".
#4-Si no encuentra a ningun usuario se cierra las "conexiones" de la Raspi(GPIO.cleanup()) y vuelta a empezar
#el bucle tras esperar 5s, hasta que encuentre un asuario asociado a este invernadero.
#5-Si encuentra a un asuario asociado a este invernadero pasa lo siguiente:
#5.1-Se recoge la planta que esta utilizando actualmente en el invernadero el usuario.
#5.2-Se llama a la funcion "procesoLed()" para comprobar si hay que ejecutar las LEDS o no.
#5.3-Se llama a la funcion "procesoVentilador()" para comprobar si hay que ejecutar el ventilador o no.
#5.4-Se hace un "connection.commit()" para que los "update" se ejecuten correctamente y se haga el cambio en la BBDD.
#6-Salimos del IF y cerramos las "conexiones" de la Raspi(GPIO.cleanup()) y vuelta a empezar tras esperar 5s.
while True:
    
    GPIO.setmode(GPIO.BCM)

    usuario =recogerUsuario()
    if usuario != None:
        planta = recogerPlanta(usuario)
        procesoLed(planta)
        procesoVentilador(planta)
        #cerrarConexion()
        connection.commit()

    GPIO.cleanup()

    time.sleep(5)

