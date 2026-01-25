import socket 

def run_client (): 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # utilizo la funcion socket.socket () para crear un objeto socket TCP que sirva 
    # como punto de contacto del cliente con el servidor
    
    # CONEXION AL SOCKET DEL SERVIDOR 
    IP = "127.0.0.1" # remplaza con la dirrecion de IP del servidor 
    PORT = 8000  # remplaza con el numero de puerto del servidor 
    
    # se establece una conexion con el servidor utilizando el metodo connect en el objeto de socket cliente 
    # NO SE ASIGNA UNA IP O PUERTO ESPECIFICO 
    # CONNECT DIRECTAMENTE VA A ELEGIR UN PUERTO QUE ESTE LIBRE Y UNA DIRRECION IP QUE PROPORCIONE LA MEJOR RUTA AL SERVIDOR DESDE LAS INTERFACES DE RED DEL SISTEMA (127.0.0.1)
    client.connect((IP,PORT))

    # BUCLE DE COMUNICACION 
    while True: 
        # input para enviar el mensaje al servidor 
        mensaje = input ("Ingrese su mensaje: ")
        client.send (mensaje.encode("utf-8")) [:1024]   
        # se inicia un bucle infinito de comunicacion con el servidor
        # la codificamos a bytes y la recortamos para que tenga 1024 bytes como maximo
        # y enviamos la informacion al servidor usando send()
        
    
        # MANEJAR RESPUESTA DEL SERVIDOR 
        
        # recibir mensaje de el servidor 
        recibir = client.recv(1024)
        recibir = recibir.decode("utf-8")\
        
        # si el servidor recibe close va a cerrar el bucle y cerramos nuestro socket 
        if recibir.lower() == "close": 
            break 
        
        print (f"Recibido = {recibir}") 
        
        # LIBERAMOS RECURSOS 

        client.close()
        print ("La conexion con el servidor finalizo")
        
run_client() 
        
    