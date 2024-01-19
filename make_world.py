import random


def make_world(filename):
    with open(f"data/{filename}", "w") as f:
        n = 150
        mapa = [[0] * n for i in range(n)]
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
        junglec = random.randint(0, 9)
        dezertc = junglec
        while junglec == dezertc:
            dezertc = random.randint(0, 9)
        snowc = junglec
        while snowc == junglec or snowc == dezertc:
            snowc = random.randint(0, 9)
        for i in range(n):
            for j in range(n):
                randmx = random.randint(-3, 3)
                randpx = random.randint(-3, 3)
                if int(n * snowc / 10) + randpx < j < int(n * (snowc / 10 + 0.1)) + randmx:
                    if mapa[i][j]:
                        mapa[i][j] = 4
                randmx = random.randint(-3, 3)
                randpx = random.randint(-3, 3)
                if int(n * junglec / 10) + randpx < j < int(n * (junglec / 10 + 0.1)) + randmx:
                    if mapa[i][j] == 1:
                        mapa[i][j] = 6
                    elif mapa[i][j] == 3:
                        mapa[i][j] = 7
                randmx = random.randint(-3, 3)
                randpx = random.randint(-3, 3)
                if int(n * dezertc / 10) + randpx < j < int(n * (dezertc / 10 + 0.1)) + randmx:
                    if mapa[i][j]:
                        mapa[i][j] = 8
        for i in range(n):
            for j in range(n):
                if mapa[i][j] == 1 or mapa[i][j] == 6 or mapa[i][j] == 4:
                    mapa[i][j] = random.choice(
                        [mapa[i][j], random.choice([mapa[i][j], random.choice([mapa[i][j], 2])])])
                if mapa[i][j] == 8:
                    mapa[i][j] = random.choice(
                        [mapa[i][j], random.choice([mapa[i][j], random.choice([mapa[i][j], 5])])])
        mapa[int(n * 0.2)][int(n / 2)] = 9
        f.writelines("\n".join(["".join([str(j) for j in mapa[i]]) for i in range(len(mapa))]))
