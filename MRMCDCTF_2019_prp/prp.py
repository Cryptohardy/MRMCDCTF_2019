from hashlib import sha256
from os import urandom as gen
from sys import stdin
from sys import stdout
from secret import flag



# this is provable PRF!
def f(k,x):
    return sha256((k+x)).digest()[:LEN]


class Feistel:
    def __init__(self):
        self.k1 = gen(LEN)
        self.k2 = self.k1
        self.k3 = self.k1

    def xor(self,x,y):
        return bytes([x[i]^y[i] for i in range(LEN)])
    
    def enc(self,p):
        assert(len(p) == 32)
        p  = p[:16],p[16:]
        L,R = p
        L,R = R,self.xor(L, f(self.k1,R))
        L,R = R,self.xor(R, f(self.k2,L))
        L,R = R,self.xor(L, f(self.k3,R))
        return L+R
    
    def dec(self,c):
        assert(len(c) == 32)
        c  = c[:16],c[16:]
        L,R = c
        L,R = R,self.xor(L, f(self.k3,R))
        L,R = R,self.xor(R, f(self.k2,L))
        L,R = R,self.xor(L, f(self.k1,R))
        return L+R

class IdealCipher:
    def __init__(self):
        self.encd  = {}
        self.decd  = {}
    def enc(self,p):
        assert(len(p) == 32)
        c = b''
        if p in self.encd:
            c = self.encd[p]
        else:
            c = gen(32)
            while c in self.decd:
                c = gen(32)
            self.encd[p] = c
            self.decd[c] = p
        return c
    def dec(self,c): 
        assert(len(c) == 32)
        p = b''
        if c in self.decd:
            p = self.decd[c]
        else:
            p = gen(32)
            while p in self.encd:
                p = gen(32)
            self.encd[p] = c
            self.decd[c] = p
        return p

def print_help():
    stdout.write("""Welcome player. 
This is the SPRP game. Long story short:
You can:
Tell me which bit of the flag we are playing over:
    f<num between 0 and %d>
Ask me to encrypt a message:
    e<32 bytes in hex>
Ask me to decrypt a message:
    d<32 bytes in hex>
    """%(len(flag)*8))


def flag_bit(idx):

    return (flag[idx//8]>>(idx%8))&1

def prp_server():
    print_help()
    bidx = 0
    b = flag_bit(bidx)


    F = Feistel()
    IC = IdealCipher()

    while True:
        cmd = stdin.readline().strip()
        assert(len(cmd)>1)
        if cmd[0] == 'f':
            # we do a complete reinit
            bidx = int(cmd[1:])
            stdout.write("ok we are now playing for bit:" + str(bidx) + "\n")
            b = flag_bit(bidx)
            stdout.write("The b at %d: "%bidx +str(b)+ "\n")
            F = Feistel()
            IC = IdealCipher()
        #encryption oracle
        if cmd[0] == 'e':
             p = bytes.fromhex(cmd[1:])
             c0 = F.enc(p)
             c1 = IC.enc(p)
             if b == 1:
                stdout.write(c1.hex()+"\n")
             else:
                stdout.write(c0.hex()+"\n")
             stdout.flush()
        #decryption oracle
        if cmd[0] == 'd':
            c = bytes.fromhex(cmd[1:])
            assert(len(c) == 32)
            p0 = F.dec(c)
            p1 = IC.dec(c)
            if b == 1:
               stdout.write(p1.hex()+"\n")
            else:
               stdout.write(p0.hex()+"\n")
            stdout.flush()



prp_server()
