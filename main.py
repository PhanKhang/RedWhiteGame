import numpy;

letterTonumb = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8

}
numbToLetter = dict([[v, k] for k, v in letterTonumb.items()])

gameMap = numpy.zeros((12, 8))


# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4
def pervayaYacheyka(rotation):
    swithcer = {
        1: 1,
        2: 2,
        3: 2,
        4: 1,
        5: 3,
        6: 4,
        7: 4,
        8: 3
    }
    return swithcer.get(rotation, 0);


def vtorayYacheyka(rotation):
    swithcer = {
        1: 2,
        2: 1,
        3: 1,
        4: 2,
        5: 4,
        6: 3,
        7: 3,
        8: 5
    }
    return swithcer.get(rotation, 0);


def place(i, j, rotation):
    gameMap[j][i] = pervayaYacheyka(rotation)
    if rotation % 2 != 0:
        gameMap[j][i + 1] = vtorayYacheyka(rotation)
    else:
        gameMap[j+1][i] = vtorayYacheyka(rotation)
    return;


def validator(str):
    if int(str[:1]) == 0:
        print("Its a normal move")
        if int(str[1:2]) % 2 != 0:
            print("Card is horisontal")
            i = letterTonumb.get(str[2:3]) - 1
            j = int(str[3:]) - 1
            print("{} {}".format(i, j))
            if 0<=i<=7 and 0<=j<=11 and 0<=i+1<=7:
                if gameMap[j][i] == 0 and gameMap[j][i + 1] == 0:
                    print("place is free")
                    if j == 0:  # first line is always supported
                        return True
                        # place(i, j, int(str[1:2]))
                    else:
                        if gameMap[j - 1][i] != 0 and gameMap[   - 1][i + 1] != 0:
                            return True;
                            # place(i, j, int(str[1:2]))
                else:
                    print("not free {} and {}".format(gameMap[j][i], gameMap[j][i + 1]))
        else:
            print("Card is vertical")
            i = letterTonumb.get(str[2:3]) - 1
            j = int(str[3:]) - 1
            print("{} {}".format(i, j))
            if 0<=i<=7 and 0<=j<=11 and 0<=j+1<=11:
                if gameMap[j][i] == 0 and gameMap[j+1][i] == 0:
                    print("place is free")
                    if j == 0:  # first line is always supported
                        # place(i, j, int(str[1:2]))
                        return True
                    else:
                        if gameMap[j - 1][i] != 0:
                            # place(i, j, int(str[1:2]))
                            return True
                else:
                    print("not free {} and {}".format(gameMap[j][i], gameMap[j + 1][i]))

    else:
        print("wrong format")

    return False;


# input_var = input("Enter something: ")
# validator(input_var)
# # print(gameMap)
# print(numpy.flipud(gameMap))
# input_var = input("Enter something: ")
# validator(input_var)
# # print(gameMap)
# print(numpy.flipud(gameMap))

for i in range (3):
    input_var = input("Enter something: ")
    if validator(input_var):
        i = letterTonumb.get(input_var[2:3]) - 1
        j = int(input_var[3:]) - 1
        place(i, j)
        print(numpy.flipud(gameMap))