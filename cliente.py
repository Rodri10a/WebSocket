import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 55123

def conectar():
    while True:
        try:
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((HOST, PORT))  #intenta conectar al servidor 
            return socket
        except:
            print("Conectando al servidor...")
            time.sleep(3)

def recibir(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                print("\nServidor desconectado. Reconectando...")
                return False
            print(mensaje)
        except:
            print("\nError de conexión. Reconectando...")
            return False

# Conectar
cliente = conectar()
print("Conectado!")

# Enviar nombre
nombre = input(cliente.recv(1024).decode())
cliente.send(nombre.encode())
print("Escribe tus mensajes (/salir para salir):\n")

# Iniciar hilo de recepción
conectado = True
def recibir_loop():
    global cliente, conectado
    while True:
        if not recibir(cliente):
            conectado = False
            cliente.close()
            cliente = conectar()
            cliente.send(nombre.encode())
            conectado = True

threading.Thread(target=recibir_loop, daemon=True).start() 

# Enviar mensajes
try:
    while True:
        mensaje = input()
        if mensaje == "/salir":
            cliente.send(mensaje.encode("utf-8"))
            break
        try:
            cliente.send(mensaje.encode())
        except:
            print("Esperando reconexión...")
            time.sleep(1)
except KeyboardInterrupt:
    print("\nCerrando...")
finally:
    cliente.close()