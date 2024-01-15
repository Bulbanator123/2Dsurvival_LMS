import random


def make_world(filename):
    with open(filename, "w") as f:
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
                    mapa[i][j] = random.choice([1, random.choice([1, random.choice([2, 1])])])
        mapa[int(n * 0.2)][int(n / 2)] = 9
        f.writelines("\n".join(["".join([str(j) for j in i]) for i in mapa]))



make_world("data/level1.txt")
