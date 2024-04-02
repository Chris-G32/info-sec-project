class PasswordInfo:
    def __init__(self,user,password,site):
        self.user=user
        self.password=password
        self.site=site
# character entropy
# 1 for 4 2 for up to the 8th and then
# 9 to 20 are 1.5
# 21
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

