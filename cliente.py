
import socket
import tqdm
import os
import random
from time import time
import logging
import datetime


#host = "localhost"
host = '192.168.0.8'
port = 5996


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step


s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

received = s.recv(BUFFER_SIZE).decode()
#print("recibi: ",received)

start_time = time()

filename, filesize = received.split(SEPARATOR)

numAle = random.randint(0,1000)

#filename = './ArchivosRecibidos/'+str(filename.split('/')[2]+str(numAle))
filename = './ArchivosRecibidos/'+'cliente'+str(numAle)+'-prueba.txt'
#filename = os.path.basename(filename)

filesize = int(filesize)

print(filename)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = s.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
        
elapsed_time = time() - start_time
print('/////////////////////////////')
print("Elapsed time: %.10f seconds." % elapsed_time)
print('/////////////////////////////')

s.close()

#Log
fecha = datetime.datetime.today()
fechaLog = fecha.strftime("%Y-%b-%d-%H-%M-%S")

logging.basicConfig( level=logging.DEBUG, filename="./logs/cliente/"+str(fechaLog)+".log")

#contenido log
logging.debug(fechaLog)
logging.debug(f'Nombre: {filename} - Tamanio: {filesize}')
logging.debug(f'tiempo: {elapsed_time}')
logging.debug(f'Entrega recibida Exitosa')


