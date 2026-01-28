import socket
import threading
import signal
import sys

# donde va a escuchar el servidor
HOST = '127.0.0.1'
PORT = 55123

# creo mi socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # protocolo TCP 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilizar la dirreccion inmediatamente 

server.bind((HOST, PORT)) # asocio al socket 
server.listen() # se pone en escucha para aceptar conexiones 
server.settimeout(1)  # Timeout para responder a Ctrl+C, es para que el servidor no se quede bloqueado
print(f"Servidor escuchando en {HOST}:{PORT}")
print("Presiona Ctrl+C para cerrar")

clientes = {}  # socket del cliente -> nombre del usuario 
servidor_corriendo = True 

def cerrar_servidor(sig, frame):
    global servidor_corriendo # para acceder a su variable global
    print("\n\nCerrando servidor...")
    servidor_corriendo = False # detiene el bucle principal 
    server.close()
    sys.exit(0) # termina el programa 

signal.signal(signal.SIGINT, cerrar_servidor)

def broadcast(mensaje):
    for cliente in list(clientes.keys()):
        try:
            cliente.send(mensaje)
        except:
            pass

def handle(cliente):
    nombre = None
    try:
        # Pedir nombre
        cliente.send("Nombre: ".encode("utf-8"))
        nombre = cliente.recv(1024).decode("utf-8").strip()
        clientes[cliente] = nombre
        
        print(f"[+] {nombre} conectado")
        broadcast(f"{nombre} entró al chat".encode("utf-8"))
        
        # Recibir mensajes
        while True:
            mensaje = cliente.recv(1024).decode("utf-8").strip()
            if not mensaje or mensaje == "/salir":
                break
            print(f"{nombre}: {mensaje}")
            broadcast(f"{nombre}: {mensaje}".encode("utf-8"))
            
    except:
        pass
    finally:
        if cliente in clientes:
            print(f"[-] {clientes[cliente]} desconectado")
            broadcast(f"{clientes[cliente]} salió".encode("utf-8"))
            del clientes[cliente]
        cliente.close()

while servidor_corriendo:
    try:
        cliente, _ = server.accept()
        threading.Thread(target=handle, args=(cliente,), daemon=True).start() 
    except socket.timeout:
        continue
    except:
        break