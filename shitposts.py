import random

def pasta(pasta_path, r):
    f = open(pasta_path)
    pastas = len(f.readlines())
    while r[0] == r[1] or r[0] == r[2]:
        r[0] = random.randint(0, pastas - 1)
    r[2] = r[1]
    r[1] = r[0]
    longstr = ''
    sendtick = 0
    endtick = 0
    for line in f:
        if endtick == 0:
            if sendtick == r[0]:
                longstr = line
                endtick = 1
                message = longstr
            elif sendtick != r[0]:
                sendtick += 1              
    f.close
    return message