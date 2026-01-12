from age import cli
import functions

def encr(username, con):
    curs = con.cursor()
    users = list(username)
    res = curs.execute("SELECT publickey FROM receivers WHERE name = ?", users)
    key = res.fetchone()[0]
    key = (key,)
    infile = functions.fchoose("rb")
    outfile = functions.fchoose("wb")
    cli.encrypt(key, infile, outfile)
