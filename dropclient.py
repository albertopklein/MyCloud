import socket
import glob
import os.path

def Main():
    host = '192.168.0.101'
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    print "Bem vindo ao sua nuvem pessoal: Dropbox:"
    print "Insira Login: "
    login = raw_input()
    s.send(login)
    serv_ans = s.recv(1024)
    if serv_ans[:2] == 'OK':
        print "Login aceito!"
        print "Senha:"
        senha = raw_input()
        s.send(senha)
        serv_ans= s.recv(1024)
        if serv_ans[:2] == 'OK':
            print "Login Efetuado com sucesso!"
            print "Lista de arquivos"
            sfilesoncloud = s.recv(1024)
            print filesoncloud
            filename = raw_input("Filename? -> ")
            if filename != 'q':
                s.send(filename)
                data = s.recv(1024)
                if data[:7] == 'EXISTE:':
                    filesize = long(data[7:])
                    message = raw_input("Arquivo encontrado, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
                    if message == 'Y' :
                        s.send("OK")
                        f = open('new_'+filename, 'wb')
                        data = s.recv(1024)
                        totalRecv = len(data)
                        f.write(data)
                        while totalRecv < filesize:
                            data = s.recv(1024)
                            totalRecv += len(data)
                            f.write(data)
                            print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                        print "Download Complete!"
                        f.close()
                else:
                    print "File Does Not Exist!"
        else:
            print "Erro no Login! Tente novamente..."

    s.close()

   

if __name__ == '__main__':
    Main()