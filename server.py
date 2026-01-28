import socket
import threading 
import signal # sirve para detectar señales del sistema 
import sys # para interactuar con el interprete de python 

# donde va a escuchar el servidor 
HOST = '127.0.0.1'
PORT = 55123

# creo mi socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # protocolo TCP IPv4 
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

# registra cuando tocas ctrl+C
signal.signal(signal.SIGINT, cerrar_servidor) 


def broadcast(mensaje):
    for cliente in list(clientes.keys()):
        try:
            cliente.send(mensaje) # intenta enviar mensaje
        except:
            # si hay error, simplemente continua 
            pass

def handle(cliente): # manejar cada cliente 
    nombre = None
    try:
        # Pedir nombre
        cliente.send("Nombre: ".encode("utf-8")) # envia pregunta 
        nombre = cliente.recv(1024).decode("utf-8").strip() # recibe propuesta 
        clientes[cliente] = nombre # guarda el cliente en el diccionario 
        
        # notifica al servidor y a todos los clientes 
        print(f"[+] {nombre} conectado") 
        broadcast(f"{nombre} entró al chat".encode("utf-8")) 
        
        # Recibir mensajes del cliente 
        while True:
            mensaje = cliente.recv(1024).decode("utf-8").strip() 
            if not mensaje or mensaje == "/salir": # si no hay mensaje o escribe /salir, termina 
                break
            print(f"{nombre}: {mensaje}")
            broadcast(f"{nombre}: {mensaje}".encode("utf-8")) # envia el mensaje a todos los demas clientes 
            
    except:
        # si hay cualquier error de conexion, sale del try 
        pass
    finally: # finally es la limpieza obligatoria, basicamente se ejecuta siempre pase lo que pase 
        # esto siempre se ejecuta al salir 
        if cliente in clientes:
            print(f"[-] {clientes[cliente]} desconectado")
            broadcast(f"{clientes[cliente]} salió".encode("utf-8")) 
            del clientes[cliente] # elimina del diccionario 
        cliente.close() # cierra conexion 

# bucle principal 
while servidor_corriendo:
    try:
        # se espera a que se conecte 
        cliente, _ = server.accept() 
        
        # se crea un hilo para manejar a este cliente 
        # daemon= True hace que el hilo se cierre cuando termine el programa 
        threading.Thread(target=handle, args=(cliente,), daemon=True).start() 
    except socket.timeout:
        # esto permite verificar si el servidor_corriendo sigue siendo True 
        continue
    except:
        # cualquier otro error, sale del bucle 
        break