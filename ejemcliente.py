import socket 
import threading

HOST = '127.0.0.1'
PORT = 55123
 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Intento de conexión inicial 
try:
    cliente.connect((HOST, PORT))
except ConnectionRefusedError as e:
    print(f"No se pudo conectar: {e}")  
    exit()

# HILO DE RECEPCIÓN: Función para estar siempre escuchando al servidor
def recibir():
    try:
        while True:
            mensaje = cliente.recv(1024) # Si el servidor manda algo, lo recibimos aquí
            if not mensaje:
                break
            print(mensaje.decode()) # Convertimos los bytes a texto y los mostramos
    except:
        print("Error en recepción.")
    finally:
        cliente.close() 

# Iniciamos el hilo de recepción para que "print" no bloquee al "input"
thread = threading.Thread(target=recibir, daemon=True)
thread.start() 

# BUCLE PRINCIPAL: Aquí es donde tú escribes
try:
    while True:
        mensaje = input() # Espera a que escribas algo y des ENTER
        if mensaje.lower() == "/salir":
            cliente.send("Usuario ha salido del chat.".encode())
            break
        cliente.send(mensaje.encode()) # Convierte tu texto a bytes y lo manda
finally:
    cliente.close()