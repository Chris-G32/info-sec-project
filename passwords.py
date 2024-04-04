import secrets
from cryptography.hazmat.primitives.kdf import pbkdf2
from cryptography.hazmat.primitives.hashes import SHA256
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
class PasswordInfo:
    def __init__(self,user,password,site):
        self.user=user
        self.password=password
        self.site=site
# character entropy
# 1 for 4 2 for up to the 8th and then
# 9 to 20 are 1.5
# 21
def generate_key(password_plaintext):
    # pbkdf2.PBKDF2HMAC(SHA256(),32,)
    kdf = pbkdf2.PBKDF2HMAC(                                                                               # Sets up the PBKDF2 Algorithm for generating the key
        algorithm=SHA256(),
        length=128,salt=b'\x13\xaf',iterations=10000
    )
    return kdf.derive(bytes(password_plaintext,'utf-8'))
def encrypt_pass(password_plaintext):
    pass
def evaluateStrength(inp:str):
    MIN_SCORE=20
    score=0
    for i in range(1,len(inp)+1):
        if(i==1):
            score+=4
        elif i<=8:
            score+=2
        elif i<=20:
            score+=1.5
        else:
            score+=1

    if(not (inp.islower() or inp.isupper())):
        score+=2
    if any(i.isnumeric() for i in inp):
        score+=2
    if(not inp.isalnum()):
        score+=2
    return score

def generate_password():
    pass
k=generate_key("password")
print(k.hex())
# 097b5b68c74d6782439710c038c1bd6e159033ce938f2b78479b88194986b161