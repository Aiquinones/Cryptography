#%% imports necesarios
import gnupg
#%% función para generar los keyrings usados
def generate_key(gpg, email, password=None):
    if password:
        gen_input_data = gpg.gen_key_input(name_real=email, name_comment=email,
        name_email=email, passphrase=password)
    else:
        gen_input_data = gpg.gen_key_input(name_real=email, name_comment=email,
        name_email=email)

    key = gpg.gen_key(gen_input_data)
    return key.fingerprint

def pre_gen_key(mail, password, server=False):
        name = mail.split("@")[0]
        if server:
                gpg = gnupg.GPG(gnupghome="gpg/server")
        else:
                gpg = gnupg.GPG(gnupghome=f"gpg/client/{name}")
                
        fingerprint = generate_key(gpg, mail, password)
        gpg.send_keys('pgp.mit.edu', fingerprint)

#%% crea los keyrings
accounts = [
        ("aiquinones@test.cl", "passaq"),
        ("alice@test.cl", "passalice"),
        ("bob@test.cl", "passbob"),
        ("charles@test.cl", "passcharles"),
        ("diana@test.cl", "passdiana"),
        ("ernest@test.cl", "passernest"),
        ("foxtrot@test.cl", "passfoxtrot")
]

for mail, password in accounts:
        pre_gen_key(mail, password)
        
pre_gen_key("server@test.cl", "server", server=True)


#%%
for mail, _ in accounts:
        name = mail.split("@")[0]
        print(name)
        gpg = gnupg.GPG(gnupghome=f"gpg/client/{name}")

        fingerprint = gpg.list_keys()[0]["fingerprint"]

        while True:
                sr = gpg.send_keys('pgp.mit.edu', fingerprint)

                print(f'stderr: {sr.stderr}')
                if "sending key" in sr.stderr:
                        break

#%%
gpg = gnupg.GPG(gnupghome=f"gpg/server")
fingerprint = gpg.list_keys()[0]["fingerprint"]
print(fingerprint)
while True:
        sr = gpg.send_keys('pgp.mit.edu', fingerprint)

        print(f'stderr: {sr.stderr}')
        if "sending key" in sr.stderr:
                break

#%%
