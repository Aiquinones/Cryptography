from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import gnupg
import random
import getpass

HOST = ''
PORT =  33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

LOCAL_MODE = False

server_fingerprint = "E7150A771F4E7FA6898F177B09093B5679F3B049"

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

def receive(password):
    # Thread corre siempre, recibiendo mensajes y mostrándolos
    while True:
        try:
            enc = client_socket.recv(BUFSIZ).decode("utf8")
            msg = str(gpg.decrypt(enc, passphrase=password))
            msg_list.insert(tkinter.END, msg)
        except OSError: 
            break

def send(event=None, msg=None):
    # Envía un mensaje encriptado al servidor, para ser distribuido
    if not msg:
        msg = my_msg.get()
        my_msg.set("")
    
    enc = str(gpg_server.encrypt(msg, "server", always_trust=True))
    client_socket.send(bytes(enc, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


def check_user(mail, password):
    # Se realiza un chequeo fácil de que el usuario tiene la clave privada
    try:
        checker = "checking"
        enc = gpg.encrypt(checker, mail, always_trust=True)
        dec = gpg.decrypt(str(enc), passphrase=password)
        return checker == str(dec)
    except:
        print("error")
        return False


def login(mail):
    # Chequeo del usuario localmente..
    password = "dummy"
    check = check_user(mail, password)
    if not check:
        password = getpass.getpass("clave:")
        check = check_user(mail, password)

    if not check:
        print("Hubo un error! Por favor revisa tu mail y contraseña")
        exit()
    
    return password


def verify(mail, password):

    # Le mandamos al servidor nuestro mail y fingerprint, para que nos registre
    # y consiga nuestra llave pública
    key = where(gpg.list_keys(), lambda key: mail in key["uids"][0])[0]
    fingerprint = key["fingerprint"]
    load = fingerprint + "---" + mail

    load_enc = str(gpg_server.encrypt(load, server_fingerprint, always_trust=True))

    # Recibo desafío, desencriptarlo me verifica.
    client_socket.send(bytes(load_enc, "utf8"))
    challenge_client = client_socket.recv(BUFSIZ).decode("utf8")
    answer = str(gpg.decrypt(challenge_client, passphrase=password))
    client_socket.send(bytes(answer, "utf8"))

    verified = client_socket.recv(BUFSIZ).decode("utf8")
    if verified == "False":
        print("El usuario no pudo ser verificado")
        return False
    print("Usuario verificado..")
    
    # Ahora verificamos que el servidor efectivamente es el servidor
    challenge_answer = str(random.randint(1000, 10000))
    challenge = str(gpg_server.encrypt(challenge_answer, server_fingerprint, always_trust=True))
    client_socket.send(bytes(challenge, "utf8"))
    answer = client_socket.recv(BUFSIZ).decode("utf8")

    if answer != challenge_answer:
        print("Servidor falso!")
        client_socket.send(bytes("False", "utf8"))
        return False
    client_socket.send(bytes("True", "utf8"))

    print("Servidor verificado")
    
    return True


mail = input("mail:")
name = mail.split("@")[0]

gpg = gnupg.GPG(gnupghome=f"gpg/client/{name}")

password = login(mail)

print("conectándose con el servidor...")
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if LOCAL_MODE:  
    gpg_server = gnupg.GPG(gnupghome=f"gpg/server")
else:
    # vemos si tenemos la public key del server, si no la buscamos
    try:
        key =where(gpg.list_keys(), lambda key: "server" in key["uids"][0])[0]
        print("No se pudo obtener la llave localmente..")
    except:
        print("buscando en el servidor..")
        download(gpg, server_fingerprint)
    gpg_server = gnupg.GPG(gnupghome=f"gpg/client/{name}")

if not verify(mail, password):
    print("El cliente o servidor no pudieron ser verificados."+
    "O eres un hacker o te están hackeando")
    exit()

# Iniciar interfaz

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive, args=(password,))
receive_thread.start()
tkinter.mainloop()
