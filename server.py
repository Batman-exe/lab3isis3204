import socket
import tqdm
import os
import threading
import random
import logging
import datetime
from time import time


#SERVER_HOST = 'localhost'
SERVER_HOST = '192.168.0.8'
SERVER_PORT = 5996

# receive 4096 bytes each time
#BUFFER_SIZE = 4096
#SEPARATOR = "<SEPARATOR>"

# datos para el envio
#filename = "./archivo/pr250.txt"
#filesize = os.path.getsize(filename)


nClientes = input("cuantos clientes quieres atender?")

tipoArchivo = int( input("archivo a transmitir: \n 1. 100mb \n 2. 250mb") )



# datos para el envio
filename = "./archivo/pr100.txt"
if tipoArchivo!=1: 
    filename = "./archivo/pr250.txt"
    
filesize = os.path.getsize(filename)

s = socket.socket()

print('Server started!')
print('Waiting for clients...')

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(25)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

cRemaing = int(nClientes)



#Log
fecha = datetime.datetime.today()
fechaLog = fecha.strftime("%Y-%b-%d-%H-%M-%S")
logging.basicConfig( level=logging.DEBUG, filename="./logs/server/"+str(fechaLog)+".log")

#contenido log
logging.debug(fechaLog)
logging.debug(f'Nombre: {filename} - Tamanio: {filesize}')
logging.debug(f'///////////////////////////////////')


# funcion para el hilo - para enviar archivo a cada cliente
def on_new_client(clientsocket,addr):
    
    start_time = time()
    
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    
    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
        # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            client_socket.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))  
        
        
        client_socket.close()
   
        elapsed_time = time() - start_time

        logging.debug(f'Cliente: {clientsocket}')
        logging.debug(f'Cliente Direccion: {addr}')
        logging.debug("Elapsed time: %.10f seconds." % elapsed_time)
        logging.debug(f'Entrega Exitosa al cliente')
        logging.debug(f'///////////////////////////////////')

        
        #s.close()


while cRemaing > 0: 
    # accept connection if there is any
    client_socket, address = s.accept()
    
    print('/////////////////////////////')
    print('/////////////////////////////')
    
    print(f"[+] {address} is connected.")    
    
    on_new_client(client_socket,address)
    
    cRemaing = cRemaing-1
    print("Faltantes: ",cRemaing)
    
    
s.close()






















