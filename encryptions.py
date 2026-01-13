from age import cli
import functions
from age.keys import agekey

def encr(username, con,infile,outfile):
    curs = con.cursor()
    users = list(username)
    res = curs.execute("SELECT publickey FROM receivers WHERE name = ?", users)
    key = res.fetchone()[0]
    key = (key,)
    cli.encrypt(key, infile, outfile)

def derive_publikey(privkey):
    if type(privkey) == string():
        key = agekey.AgePrivateKey.from_private_string(privkey)
        return key.public_key().public_string()

def generate_keypair():
    key = agekey.AgePrivateKey.generate()
    privkey = key.private_string()
    publikey = key.public_key().public_string()
    return (publikey, privkey)