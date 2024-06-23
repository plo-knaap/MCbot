import random

def pasta(pasta_path, pastas, r):
    f = open(pasta_path)
    while r[0] == r[1] or r[0] == r[2]:
        r[0] = random.randint(0, pastas - 1)
    r[2] = r[1]
    r[1] = r[0]
    longstr = ''
    sendtick = 0
    endtick = 0
    for line in f:
        if endtick == 0:
            if line != '\n' and sendtick == r[0]:
                longstr = line
                endtick = 1
                message = longstr
            elif line != '\n' and sendtick != r[0]:
                sendtick += 1              
    f.close
    return message