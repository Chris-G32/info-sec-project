import hashlib
from cryptography.hazmat.primitives.kdf import pbkdf2
from cryptography.hazmat.primitives.hashes import SHA256
from Crypto.Cipher import AES
import secrets
#Enum class for password strength scores
class PasswordStrength:
    OK=20
    STRONG = 26
    EXCELLENT = 30

#Provides utilities, mainly for evaluating password scores
class PasswordUtils:
    def score_password_strength(inp:str):
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
    def is_excellent(score:int):
        return score >= PasswordStrength.EXCELLENT
    def is_strong(score:int):
        return score >= PasswordStrength.STRONG
    def is_ok(score:int):
        return score >= PasswordStrength.OK
    def is_weak(score:int):
        return score < PasswordStrength.OK
    def hash_password(pw:str):
        return hashlib.sha256(bytes(pw,'utf-8'),usedforsecurity=True).digest()
    
    def encrypt(pw:str,plaintext:str):
        key=PasswordUtils.keygen(pw)
        cipher = AES.new(key, AES.MODE_CFB)
        cipher_text = cipher.encrypt(bytes(plaintext,'utf-8'))
        iv=cipher.iv
        return (cipher_text,iv)
    def decrypt(pw:str,cipher_text:str,iv):
        key=PasswordUtils.keygen(pw)
        decrypt_cipher = AES.new(key, AES.MODE_CFB,iv=iv)
        plaintext = decrypt_cipher.decrypt(cipher_text).decode("utf-8")
        return plaintext
    def keygen(pw:str):
        kdf = pbkdf2.PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,salt=b'\x13\xaf',iterations=10000
        )
        return kdf.derive(bytes(pw,'utf-8'))
    def generate_password():
        numgen=secrets.SystemRandom()
        PASS_LENGTH=16
        generated=''
        while(not PasswordUtils.is_excellent(PasswordUtils.score_password_strength(generated))):
            generated=''
            for i in range(PASS_LENGTH):
                generated+=chr(numgen.randint(33,126))#Generate random ascii value
        return generated