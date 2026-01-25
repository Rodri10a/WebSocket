import socket
import threading

HOST = '127.0.0.1' # Dirección local (tu propia PC)
PORT = 55123       # Puerto de escucha

# Crea el socket y lo pone a escuchar en la red
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT)) 
server.listen()
print(f"Servidor escuchando en {HOST}:{PORT}")

clientes = [] # Lista para almacenar los objetos socket de cada usuario conectado

# Función "Broadcast": Envía un mensaje a TODOS los clientes en la lista
def broadcast(mensaje):
    for cliente in clientes[:]: # Recorre una copia de la lista para evitar errores al eliminar
        try: 
            cliente.send(mensaje)
        except:
            # Si falla el envío, el cliente ya no está, así que lo removemos
            if cliente in clientes:
                clientes.remove(cliente)

# Función "Handle": Se encarga de la conversación INDIVIDUAL con cada cliente
def handle(cliente, direccion): 
    try:
        while True:
            mensaje = cliente.recv(1024) # Espera a recibir algo de este cliente
            if not mensaje: 
                broadcast(f"{direccion} se desconectó.".encode())
                break
            
            texto = mensaje.decode()
            if texto == "Usuario ha salido del chat.":
                broadcast(f"{direccion} dejó el chat.".encode())
                break 
            
            # Si envió un mensaje normal, lo mandamos a todos
            broadcast(f"{direccion}: {texto}".encode())
    except:
        pass
    finally:
        # Limpieza: sacar al cliente de la lista y cerrar su conexión
        if cliente in clientes:
            clientes.remove(cliente)
        cliente.close()

# Función "Recibir": El bucle principal que acepta nuevas personas
def recibir():
    while True:
        cliente, direccion = server.accept() # Se queda pausado aquí hasta que alguien se conecta m
        print(f"Conectado con {direccion}")
        
        clientes.append(cliente) # Agregamos al nuevo usuario a la lista
        broadcast(f"{direccion} se ha conectado".encode()) # Avisamos a todos
        
        # CREACIÓN DEL HILO: Inicia una conversación separada para este cliente
        thread = threading.Thread(target=handle, args=(cliente, direccion), daemon=True)
        thread.start()

if __name__ == "__main__": 
    recibir()