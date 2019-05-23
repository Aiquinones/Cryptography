#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random
import gnupg

LOCAL_MODE = False

def download(gpg, fingerprint):

    while True:
            ir = gpg.recv_keys('pgp.mit.edu', fingerprint)

            print(f'stderr: {ir.stderr}')
            if "IMPORTED" in ir.stderr:
                    break

def where(list, cond):
    ans = []
    for it in list:
        if cond(it):
            ans.append(it)
    return ans

gpg = gnupg.GPG(gnupghome="gpg/server")

class UserInterface:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.mail = None
        self.fingerprint = None
        self.gpg = None
        self.name = ""


class Server:
    def __init__(self):
        self.users = []
        self.passphrase =  "server"

        self.HOST = ''
        self.PORT = 33000
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.ADDR)

    def accept_incoming_connections(self):
        # Thread constantemente escuchando por nuevos usuarios
        while True:
            socket, adress = self.socket.accept()
            user = UserInterface(address=adress, socket=socket)
            self.users.append(user)
            Thread(target=self.handle_client, args=(user,)).start()


    def verify(self, user, mail):

        # Encripto con la llave publica del usuario,  si es capaz de desencriptarla,
        # entonces efectivamente sé que es él
        print(f"verificando {mail}..")

        if LOCAL_MODE:
            user.gpg = gnupg.GPG(gnupghome=f"gpg/client/{user.name}")
        else:
            # vemos si tenemos la public key, si no la buscamos en el server
            try:
                key = where(gpg.list_keys(), lambda key: mail in key["uids"][0])[0]
            except:
                print("descargando llave..")
                download(gpg, user.fingerprint)

            user.gpg = gpg

        # Se desafía al usuario, si es realmente él, podrá desencriptar con su privada
        challenge_answer = str(random.randint(1000, 10000))
        enc = user.gpg.encrypt(challenge_answer, user.mail, always_trust=True)
        challenge_client = str(enc)
        user.socket.send(bytes(challenge_client, "utf8"))

        # Se ve el resultado de la verificación del usuario..
        answer = user.socket.recv(self.BUFSIZ).decode("utf8")
        if answer != challenge_answer:
            print("Usuario falso!")
            user.socket.send(bytes("False", "utf8"))
            return False
        user.socket.send(bytes("True", "utf8"))

        print("Usuario verificado..")

        # Ahora el usuario verifica el servidor
        challenge_server = user.socket.recv(self.BUFSIZ).decode("utf8")
        answer = str(gpg.decrypt(challenge_server, passphrase=self.passphrase))
        user.socket.send(bytes(answer, "utf8"))

        # Se ve el resultado..
        verified = user.socket.recv(self.BUFSIZ).decode("utf8")
        if verified == "False":
            print("El servidor no pudo ser verificado")
            return False
        print("Servidor verificado")

        return True


    def handle_client(self, user): 

        # El usuario solicita verificación. Envía su mail y fingerprint
        # para que el servidor pueda obtener su llave pública y nombre 
        # de usuario

        socket = user.socket
        enc_load = socket.recv(self.BUFSIZ).decode("utf8")
        load = str(gpg.decrypt(enc_load, passphrase=self.passphrase))
        fingerprint, mail = load.split("---")

        user.mail = mail
        user.fingerprint = fingerprint
        user.name = mail.split("@")[0]

        if not self.verify(user, mail):
            socket.close()
            self.users.pop(self.users.index(user))
            exit()

        # Una vez verifiaco, solo queda recibir mensajes y enviárselos al resto del
        # chat
        while True:
            enc = socket.recv(self.BUFSIZ).decode("utf8")
            msg = str(gpg.decrypt(enc, passphrase=self.passphrase))
            if msg != "{quit}":
                self.broadcast(msg, user.name)
            else:
                socket.send(bytes("{quit}", "utf8"))
                socket.close()
                self.users.pop(self.users.index(user))
                break

    def broadcast(self, msg, prefix=""):
        # Se envía un mensaje desde un cliente a todos. Se usa la llave de cada 
        # uno para encriptar por separado
        msg = prefix + ": " + msg
        for user in self.users:
            enc = str(user.gpg.encrypt(msg, user.fingerprint, always_trust=True))
            user.socket.send(bytes(enc, "utf8"))

    def main(self):
        self.socket.listen(5)
        print("Esperando una conexion...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.socket.close()

if __name__ == "__main__":
    server = Server()
    server.main()