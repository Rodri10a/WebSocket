import socket

def run_server (): 
    
    # creamos un objeto del socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # esto puede ser el host o la IP 
    IP = "127.0.0.1" # LOCALHOST 

    PORT = 8000 # numero del puerto en la que el sistema operativo identifica la aplicacion del servidor  
    
    # se usa valores mas del 1023 para evitar colisiones con los puertos utilizados por el sistema 
    
    
    # preparamos el socket para recibir conexiones vinculando a la dirrecion IP y al puerto que definimos antes 
    server.bind ((IP,PORT))
    
    
    # backlog = el numero maximo de conexiones en cola no aceptados.
    
    # escucha las conexiones entrantes 
    server.listen()
    print (f"Servidor escuchando en: {IP}: {PORT}") 
    
    # A continuacion, espera y acepta las conexiones entrantes entre clientes. El metodo "accept", detiene el hilo de ejecucion hasta que se conecte un cliente 
    
    # devuelve un par de tuplas (conn,address), address es una tupla de la direccion IP y el puerto del cliente 
    
    # accept crea un nuevo socket para comunicarse con el cliente en lugar de vincular el socket de escucha
    # (llamado server en nuestro ejemplo) a la dirección del cliente y utilizarlo para la comunicación
    client_socket, client_address = server.accept() 
    print (f"Aceptando conexion de: {client_address[0]}: {client_address[1]} " )
    
    
    
    # se inicia un bucle infinito para comunicarnos.
    # Aca se realiza una llamada al metodo recv del objeto client_socket. Este metodo recibe del cliente el numero de bytes, en este caso 1024 
    # reques esta en forma binaria, se transforma utilizando "decode". 
    # close ya seria para que se devuelva la confirmacion del cliente y finaliza su conexion 
    
    while True:
        request = client_socket.recv(1024) 
        request = request.decode("utf-8") # convierte bytes a texto normal 
        
        if request.lower() == "close": 
            # envia al cliente cual dirrecion deberia estar cerrada y rompe el bucle 
            client_socket.send("close".encode("utf-8"))
            break 
        
        print (f"Recibe: {request}") 
    
    
    # ENVIAR RESPUESTA AL CLIENTE
    # ahora se maneja la respuesta normal del servidor al cliente (cuando el cliente no desea cerar la conexion)
    
    response = "accepted".encode("utf-8") 
    client_socket.send(response) # convierte y envia el mensaje a el cliente 
    
    
    # LIBERAR RECURSOS 
    # una vez que se sale del bucle la comunicacion con el cliente ha finalizado, asi que se cierra el socket del cliente
    # utilizando el metodo close() para liberar recursos del sistema. y tambien se cerramos le socket del servidor utilizando lo mismo 
    
    client_socket.close()
    print ("La conexion con el cliente a terminado")
    server.close()
    
run_server()
    
    
    