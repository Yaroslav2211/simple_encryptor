from age import cli
import functions
from age.keys import agekey
import os

def encr(username, con,infile,outfile):
    curs = con.cursor()
    users = list(username)
    res = curs.execute("SELECT publickey FROM receivers WHERE name = ?", users)
    key = res.fetchone()[0]
    key = (key,)
    cli.encrypt(key, infile, outfile)

def decr(username,con,infile,outfile):
    curs = con.cursor()
    users = list(username)
    res = curs.execute("SELECT privkey FROM receivers WHERE name = ?", users)
    key = res.fetchone()[0]
    keyfile = open("keyfile.txt", "w")
    keyfile.write(key)
    keyfile.write("\n")
    keyfile.close()
    cli.decrypt(infile, outfile, keyfiles=("keyfile.txt",))
    os.remove("keyfile.txt")


def derive_publikey(privkey):
    if type(privkey) == string():
        key = agekey.AgePrivateKey.from_private_string(privkey)
        return key.public_key().public_string()

def generate_keypair():
    key = agekey.AgePrivateKey.generate()
    privkey = key.private_string()
    publikey = key.public_key().public_string()
    return (publikey, privkey)