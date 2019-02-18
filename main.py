#!/usr/bin/python3
import numpy
from move import Move
from validator import Validator
from appraiser import Appraiser

# convert letters to numbers
letterToNumb = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8

}
# convert numbers to letters
numbToLetter = dict([[v, k] for k, v in letterToNumb.items()])

coordinateToRotation = {}

# game map
gameMap = numpy.zeros((12, 8))

# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4
row_labels = ['12', '11', '10', '9 ', '8 ', '7 ', '6 ', '5 ', '4 ', '3 ', '2 ', '1 ']

# player 1 is colors
# player 2 is circles
validator = Validator(gameMap, coordinateToRotation)
appraiser = Appraiser(gameMap)
red = [1, 3]
white = [2, 4]
dot = [1, 4]
ring = [2, 3]


# give what is in the first half of the card according to rotation if not found return 10
def pervayaYacheyka(rotation):
    translator = {
        1: 1,
        2: 2,
        3: 2,
        4: 1,
        5: 3,
        6: 4,
        7: 4,
        8: 3
    }
    return translator.get(rotation, 10);


# give what is in the second half of the card according to rotation if not found return 10
def vtorayYacheyka(rotation):
    translator = {
        1: 2,
        2: 1,
        3: 1,
        4: 2,
        5: 4,
        6: 3,
        7: 3,
        8: 4
    }
    return translator.get(rotation, 10);


# put card at position i j and the rotation. keep in mind that coordinates are reversed j before i;


def correctPrinter(gameMap):
    print("       A    B    C    D    E    F    G    H")
    for row_label, row in zip(row_labels, numpy.flipud(gameMap)):
        print('%s [%s]' % (row_label, ' '.join('%04s' % int(i) for i in row)))


def place(move):
    if move.type == 0:
        if validator.placeValidator(move):
            i = move.targetCoordinateLet - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation;
            gameMap[j][i] = pervayaYacheyka(rotation)
            if rotation % 2 != 0:
                gameMap[j][i + 1] = vtorayYacheyka(rotation)
            else:
                gameMap[j + 1][i] = vtorayYacheyka(rotation)
            return True
        else:
            return False
    else:
        if validator.recycleValidator(move):
            i1 = move.sourceCoordinate1Let - 1
            j1 = move.sourceCoordinate1Num - 1

            i2 = move.sourceCoordinate2Let - 1
            j2 = move.sourceCoordinate2Num - 1

            old_val1 = gameMap[j1][i1]
            old_val2 = gameMap[j2][i2]

            gameMap[j1][i1] = 0
            gameMap[j2][i2] = 0

            i = move.targetCoordinateLet - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            if validator.placeValidatorCoord(i, j, rotation):
                # remove the value from dictionary of moves
                if coordinateToRotation.pop(numbToLetter.get(i1 + 1) + str(j1 + 1), 0) == 0:
                    coordinateToRotation.pop(numbToLetter.get(i2 + 1) + str(j2 + 1), 0)

                coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation
                gameMap[j][i] = pervayaYacheyka(rotation)
                if rotation % 2 != 0:
                    gameMap[j][i + 1] = vtorayYacheyka(rotation)
                else:
                    gameMap[j + 1][i] = vtorayYacheyka(rotation)
                return True
            else:
                gameMap[j1][i1] = old_val1
                gameMap[j2][i2] = old_val2
                return False
    return


def main():
    choice = int(input("Write 0 for dots and a for colors: "))
    if choice == 0:
        print("Player 1: Dots")
        print("Player 2: Colors")
    else:
        print("Player 1: Colors")
        print("Player 2: Dots")
    legal = False

    for k in range(1, 61):
        # print("Turn " + str(k) + " Player " + str((k-1) % 2+1))
        if choice == 0 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with dots")
        elif choice == 0 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with colors")
        elif choice == 1 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with colors")
        elif choice == 1 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with dots")

        # чекер на написание хода надо не хочется чтобы все ломалос
        while not legal:
            movok = False
            while not movok:
                input_var = input()
                # print(input_var)
                try:
                    move = Move(input_var)
                    movok = True
                except:
                    print("unable to parse the move, try again")
            if k <= 24 and move.type == 0:
                legal = place(move)
            elif k > 24 and move.type == 1:
                legal = place(move)
            if not legal:
                print("illegal move, try again")

        print("Current Game field")
        # print(numpy.flipud(gameMap))
        correctPrinter(gameMap)
        # print(coordinateToRotation)

        appraiser.appraise(move)
        print("Dot map")
        # print(numpy.flipud(appraiser.gameMap_dot))
        correctPrinter(appraiser.gameMap_dot)
        appraiser.getAvailableMoves(appraiser.gameMap_dot)

        print("Ring map")
        # print(numpy.flipud(appraiser.gameMap_ring))
        correctPrinter(appraiser.gameMap_ring)
        appraiser.getAvailableMoves(appraiser.gameMap_ring)

        print("White map")
        # print(numpy.flipud(appraiser.gameMap_white))
        correctPrinter(appraiser.gameMap_white)
        appraiser.getAvailableMoves(appraiser.gameMap_white)

        print("Red map")
        # print(numpy.flipud(appraiser.gameMap_red))
        correctPrinter(appraiser.gameMap_red)
        appraiser.getAvailableMoves(appraiser.gameMap_red)
        #
        #
        result = validator.victoryCheck((k + choice) % 2)
        if result != "go":
            print(result)
            break
        legal = False


main()
