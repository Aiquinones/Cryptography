
def upload(gpg):

    fingerprint = gpg.list_keys()[0]["fingerprint"]

    while True:
            sr = gpg.send_keys('pgp.mit.edu', fingerprint)

            print(f'stderr: {sr.stderr}')
            if "sending key" in sr.stderr:
                    break

def download(gpg, fingerprint):

    while True:
            ir = gpg.recv_keys('pgp.mit.edu', fingerprint)

            print(f'stderr: {ir.stderr}')
            if "sending key" in ir.stderr:
                    break
            input()

def where(list, cond):
    ans = []
    for it in list:
        if cond(it):
            ans.append(it)
    return ans