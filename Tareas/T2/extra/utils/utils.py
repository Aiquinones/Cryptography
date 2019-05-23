#%%
import gnupg
gpg = gnupg.GPG(gnupghome="gpg")

#%%
def where(list, cond):
    ans = []
    for it in list:
        if cond(it):
            ans.append(it)
    return ans

#%% generate key
def generate_key(email, password=None, name="No name", comment="No comment"):
    if password:
        gen_input_data = gpg.gen_key_input(name_real=name, name_comment=comment,
        name_email=email, passphrase=password)
    else:
        gen_input_data = gpg.gen_key_input(name_real=name, name_comment=comment,
        name_email=email)

    key = gpg.gen_key(gen_input_data)
    return key.fingerprint

#%%
def find_key_by_uid(content, private=False):
        public_keys = gpg.list_keys(private)
        def cond(key):
                for uid in key["uids"]:
                        if content in uid:
                                return True
                return False
        return where(public_keys, lambda it: cond(it))

#%%
fingerprint = generate_key("server", "server", name="server", comment="server")
