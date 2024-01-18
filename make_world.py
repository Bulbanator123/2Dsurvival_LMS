import random


def make_world(filename):
    with open(f"data/{filename}", "w") as f:
        n = 150
        mapa = [0] * n
        for i in range(n):
            mapa[i] = [0] * n
        reliev = [n * 0.3]
        for i in range(n):
            k = random.randint(-2, 3)
            reliev.append(min(max(reliev[i] + k, 0), int(n * 0.4)))
        for i in range(n):
            for j in range(n):
                if i < int(n * 0.2):
                    mapa[i][j] = 0
                elif int(n * 0.2) <= i <= int(n * 0.4):
                    if i < reliev[j]:
                        mapa[i][j] = 0
                    elif i == reliev[j]:
                        mapa[i][j] = 3
                    else:
                        mapa[i][j] = 1
                else:
                    mapa[i][j] = 1
        for i in range(n):
            for j in range(n):
                rand = random.randint(0, 3)
                if rand == 0:
                    if int(n * 0.2) < j < int(n * 0.3):
                        if mapa[i][j]:
                            mapa[i][j] = 4
                elif rand == 1:
                    if int(n * 0.2) <= j < int(n * 0.3):
                        if mapa[i][j]:
                            mapa[i][j] = 4
                elif rand == 2:
                    if int(n * 0.2) < j <= int(n * 0.3):
                        if mapa[i][j]:
                            mapa[i][j] = 4
                elif rand == 3:
                    if int(n * 0.2) <= j <= int(n * 0.3):
                        if mapa[i][j]:
                            mapa[i][j] = 4
                rand = random.randint(0, 3)
                if rand == 0:
                    if int(n * 0.7) < j < int(n * 0.8):
                        if mapa[i][j] == 1:
                            mapa[i][j] = 6
                        elif mapa[i][j] == 3:
                            mapa[i][j] = 7
                elif rand == 1:
                    if int(n * 0.7) <= j < int(n * 0.8):
                        if mapa[i][j] == 1:
                            mapa[i][j] = 6
                        elif mapa[i][j] == 3:
                            mapa[i][j] = 7
                elif rand == 2:
                    if int(n * 0.7) < j <= int(n * 0.8):
                        if mapa[i][j] == 1:
                            mapa[i][j] = 6
                        elif mapa[i][j] == 3:
                            mapa[i][j] = 7
                elif rand == 3:
                    if int(n * 0.7) <= j <= int(n * 0.8):
                        if mapa[i][j] == 1:
                            mapa[i][j] = 6
                        elif mapa[i][j] == 3:
                            mapa[i][j] = 7
        for i in range(n):
            for j in range(n):
                if mapa[i][j] == 1 or mapa[i][j] == 6 or mapa[i][j] == 4:
                    mapa[i][j] = random.choice(
                        [mapa[i][j], random.choice([mapa[i][j], random.choice([mapa[i][j], 2])])])
        mapa[int(n * 0.2)][int(n / 2)] = 9
        f.writelines("\n".join(["".join([str(j) for j in mapa[i]]) for i in range(len(mapa))]))
