import socket
import threading
import time 

# Asigna dirrecion y puerto del servidor que se conectara 
HOST = '127.0.0.1'
PORT = 55123 

# conectar con el servidor 
def conectar():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea un nuevo socket 
            s.connect((HOST, PORT))  #intenta conectar al servidor 
            return s # si tiene exito devuelve el socket 
        except:
            print("Conectando al servidor...")
            time.sleep(3) # para que cada 3 segundos intente conectar al servidor 


def recibir(cliente):
    while True:
        try:
            # intenta recibir hasta 1024 bytes del servidor 
            mensaje = cliente.recv(1024).decode("utf-8")
            if not mensaje:
                # si no recibe nada, el servidor se desconecto
                print("\nServidor desconectado. Reconectando...")
                return False
            print(mensaje)
        except:
            # si hay error de conexion 
            print("\nError de conexión. Reconectando...")
            return False

# Conectar al servidor 
cliente = conectar()
print("Conectado!")

# Enviar nombre
nombre = input(cliente.recv(1024).decode("utf-8")) 
cliente.send(nombre.encode("utf-8")) # envia el nombre al servidor 
print("Escribe tus mensajes (/salir para salir):\n") 

# Iniciar hilo de recepción
conectado = True
def recibir_loop():
    global cliente, conectado # accede a las variables globales de afuera de la funcion 
    while True:
        if not recibir(cliente): 
            conectado = False # si devuelva false, hubo desconexion 
            cliente.close() 
            cliente = conectar() # reconecta automaticamente 
            cliente.send(nombre.encode("utf-8")) # envia nuevamente el nombre al servidor 
            conectado = True


# Inicia hilo de recepcion 
# daemon= True hace que se cierre cuando termina el programa inicial 
threading.Thread(target=recibir_loop, daemon=True).start() 

# bucle principal para enviar mensajes
try:
    while True:
        mensaje = input()
        if mensaje == "/salir":
            cliente.send(mensaje.encode("utf-8"))
            break
        try: # intenta enviar el mensaje al servidor 
            cliente.send(mensaje.encode("utf-8"))
        except:
            # si falla (servidor caido), espera a que reconecte 
            print("Esperando reconexión...")
            time.sleep(1)
            
except KeyboardInterrupt: # si presionas Ctrl+C, cierra limpiamente 
    print("\nCerrando...")
finally:
    # cierra conexion 
    cliente.close()