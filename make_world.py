import random


def make_world(filename):
    with open(filename, "w") as f:
        n = 100
        mapa = [0] * n
        for i in range(n):
            mapa[i] = [0] * n
        reliev = [random.randrange(20, 41)]
        for i in range(n):
            k = random.randrange(-2, 3)
            reliev.append(min(max(reliev[i] + k, 0), 20))
        for i in range(100):
            for j in range(100):
                if i < 20:
                    mapa[i][j] = 0
                elif 20 <= i <= 40:
                    if i < 40 - reliev[j]:
                        mapa[i][j] = 0
                    else:
                        mapa[i][j] = 1
                else:
                    mapa[i][j] = random.choice([1, random.choice([1, random.choice([2, 1])])])
        for i in range(100):
            for j in range(100):
                ...
        mapa[18][50] = 9
        f.writelines("\n".join(["".join([str(j) for j in i]) for i in mapa]))



make_world("data/level1.txt")
