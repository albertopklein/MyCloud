
import socket
import threading
import os
import glob

def RetrFile(name, sock, localfiles):
    #a = os.system("ls -l")
    login = sock.recv(1024)
    if login == "Redes20172": # "Login aceito!"
        sock.send('OK') # Envia OK para cliente
        #print "Aguardando senha..."
        senha = sock.recv(1024)
        if (senha[:4] == "abcd"): # "Senha aceita!"
            sock.send('OK') # Envia OK para cliente
            # Login Efetuado com sucesso!
            sock.send(str(localfiles))
            print localfiles
            filename = sock.recv(1024)
            if os.path.isfile(filename):
                sock.send("EXISTE: " + str(os.path.getsize(filename)))
                userResponse = sock.recv(1024)
                if userResponse[:2] == 'OK':
                    with open(filename, 'rb') as f:
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
                        while bytesToSend != "":
                            bytesToSend = f.read(1024)
                            sock.send(bytesToSend)
            else:
                sock.send("ERR ")
        else:
            print "Senha incorreta!"
    sock.close()

def Main():
    host = '192.168.0.101'
    port = 5000


    s = socket.socket()
    s.bind((host,port))

    s.listen(5)
    print "Dropbox Server Started."
    localfiles = glob.glob("*")
    while True:
        c, addr = s.accept()
        print "client connedted ip:<" + str(addr) + ">"
        t = threading.Thread(target=RetrFile, args=("RetrThread", c, localfiles))
        t.start()
         
    s.close()

if __name__ == '__main__':
    Main()
