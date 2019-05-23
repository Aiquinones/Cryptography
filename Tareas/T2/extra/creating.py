#%% set up
import gnupg
from utils.utils import where, generate_key
from client.user import User
gpg = gnupg.GPG(gnupghome="gpg")


#%%
public_keys = gpg.list_keys()

#%%
result = gpg.send_keys("pgp.mit.edu", "2F16A6264DDDEE81234B1343DE74A52AA9E8EAE6")
print(result.stderr)

#%%
user = User("aiquinones@test.cl", "password")

#%%
generate_key("test3", "password")

#%%
gpg