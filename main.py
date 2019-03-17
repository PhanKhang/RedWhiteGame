#!/usr/bin/python3
import numpy
from move import Move
from validator import Validator
from appraiser import Appraiser
from placer import Placer
from treenode import Treenode
import copy
import time
import random

# game map
gameMap = numpy.zeros((12, 8))
valueMapRed = numpy.zeros((12, 8))
valueMapWhite = numpy.zeros((12, 8))
valueMapDot = numpy.zeros((12, 8))
valueMapRing = numpy.zeros((12, 8))

# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4
row_labels = ['12', '11', '10', '9 ', '8 ', '7 ', '6 ', '5 ', '4 ', '3 ', '2 ', '1 ']

# player 1 is colors
# player 2 is circles
validator = Validator()
appraiser = Appraiser()
placer = Placer()
red = [1, 3]
white = [2, 4]
dot = [1, 4]
ring = [2, 3]


def getCard(i):
    whiteB = '\033[0;37;40m'
    redB = '\033[0;37;41m'
    dot = u" \u25CF"
    ring = u" \u25EF"
    if i == 1:
        return redB + dot
    if i == 2:
        return whiteB + ring
    if i == 3:
        return redB + ring
    if i == 4:
        return whiteB + dot
    return " 0"


def getCardL(i):
    whiteB = "W"
    redB = "R"
    dot = "D"
    ring = "C"
    if i == 1:
        return redB + dot
    if i == 2:
        return whiteB + ring
    if i == 3:
        return redB + ring
    if i == 4:
        return whiteB + dot
    return " 0"


def correctPrinter(gameMap):
    print("       A    B    C    D    E    F    G    H")
    for row_label, row in zip(row_labels, numpy.flipud(gameMap)):
        print('%s [%s]' % (row_label, ' '.join('%04s' % int(i) for i in row)))


def correctPrinterMapL(gameMap):
    ENDC = '\033[2m'
    print("     A  B  C  D  E  F  G  H")
    for j in range(11, -1, -1):
        s = str(j + 1) + "\t"
        for i in range(8):
            s += getCardL(gameMap[j][i])
            s += " "
            s += ENDC
        print(s, ENDC)
    print("     A  B  C  D  E  F  G  H")


def correctPrinterMap(gameMap):
    ENDC = '\033[2m'
    print("     A   B   C   D   E   F   G   H")
    for j in range(11, -1, -1):
        s = str(j + 1) + "\t"
        for i in range(8):
            s += getCard(gameMap[j][i])
            s += "  "
            s += ENDC
        print(s, ENDC)
    print("     A   B   C   D   E   F   G   H")


def minimax(node, depth, maxP):
    if depth == 0 or node.goalState != 'go':
        return node.getOwnWeight()
    if maxP:
        # node.weight = -9999999
        weight = -9999999
        node.populateChildren()
        for childnode in node.children:
            weight = max(weight, minimax(childnode, depth - 1, False))
        node.weight = weight
        return node.weight
    else:
        weight = 9999999
        node.populateChildren()
        for childnode in node.children:
            weight = min(weight, minimax(childnode, depth - 1, True))
        node.weight = weight
        return node.weight


def alphabeta(node, depth, a, b, maxP):
    if depth == 0 or node.goalState != 'go':
        return node.getOwnWeight()
    if maxP:
        weight = -9999999
        newchildren = []
        node.populateChildren()
        for childnode in node.children:
            weight = max(weight, alphabeta(childnode, depth - 1, a, b, False))
            a = max(a, weight)
            newchildren.append(childnode)
            if a >= b:
                node.children = newchildren
                break
        node.weight = weight
        return node.weight
    else:
        weight = 9999999
        newchildren = []
        node.populateChildren()
        for childnode in node.children:
            weight = min(weight, alphabeta(childnode, depth - 1, a, b, True))
            b = min(b, weight)
            newchildren.append(childnode)
            if a >= b:
                # print("prune!")
                node.children = newchildren
                break
        node.weight = weight
        return node.weight



def main():
    # pruning = int(input("Activate alpha-beta pruning? 1 for yes 0 for no: "))
    pruning = 1
    # trace = int(input("Generate trace? 1 for yes 0 for no: "))
    # depth = int(input("Set tree depth: "))
    depth = 3
    # width = int(input("Set tree width: "))
    width = 0
    computer = int(input("Which player should be computer 1 or 2?: "))
    choice = int(input("Player 1  will be playing? 0 for dots and 1 a for colors: "))
    if choice == 0:
        print("Player 1: Dots")
        print("Player 2: Colors")
    else:
        print("Player 1: Colors")
        print("Player 2: Dots")
    legal = False

    # Appraiser().setInitialValue(valueMap)
    party = 0
    for k in range(1, 40):
        # print("Turn " + str(k) + " Player " + str((k-1) % 2+1))
        if choice == 0 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with dots")
            party = 0
        elif choice == 0 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with colors")
            party = 1
        elif choice == 1 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with colors")
            party = 1
        elif choice == 1 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with dots")
            party = 0

        maximizing = True
        if party == 1:
            maximizing = False

        while not legal:
            movok = False
            while not movok:
                input_var = ''
                if (k % 2 == 1 and computer == 1) or (k % 2 == 0 and computer == 2):
                    if k > 1:
                        start_time = time.time()
                        computer_party = party
                        treenode = Treenode(depth, valueMapRed, valueMapWhite, valueMapRing, valueMapDot, gameMap, k, validator, party, computer_party, width)
                        if pruning == 1:
                            targetWeight = alphabeta(treenode, depth, -9999999, 9999999, maximizing)
                        else:
                            targetWeight = minimax(treenode, depth, maximizing)

                        input_var = treenode.getMove(targetWeight)
                        print("--- %s seconds ---" % (time.time() - start_time))
                        print("computer move: " + input_var)
                    else:
                        input_var = "0 " + str(random.randint(1, 8)) + " " + validator.numbToLetter.get(
                            random.randint(4, 5)) + " " + str(1)
                else:
                    input_var = input()

                try:
                    move = Move(input_var)
                    movok = True
                except:
                    print("unable to parse the move, try again")
            if k <= 24 and move.type == 0:
                legal = placer.place(move, validator, gameMap)
            elif k > 24 and move.type == 1:
                legal = placer.place(move, validator, gameMap)
            if not legal:
                print("illegal move, try again")

        print("Current Game field")
        correctPrinterMap(gameMap)  # change to correctPrinterMapL for letter output
        # print(validator.coordinateToRotation)
        appraiser.appraise(move, valueMapRed, valueMapWhite, valueMapRing, valueMapDot, gameMap)

        print("Current Weight")
        print(appraiser.getScore(valueMapRed, valueMapWhite, valueMapRing, valueMapDot, party))
        # print("Red map")
        # # print(appraiser.getAvailableMoves(appraiser.getRedMap(), tmp))
        # correctPrinter(appraiser.getRedMap(valueMap))
        #
        # print("White map")
        # # print(appraiser.getAvailableMoves(appraiser.getWhiteMap(), tmp))
        # correctPrinter(appraiser.getWhiteMap(valueMap))
        #
        # print("Ring map")
        # # print(appraiser.getAvailableMoves(appraiser.getRingMap(), tmp))
        # correctPrinter(appraiser.getRingMap(valueMap))
        #
        # print("Dot map")
        # # print(appraiser.getAvailableMoves(appraiser.getDotMap(), tmp))
        # correctPrinter(appraiser.getDotMap(valueMap))

        result = validator.victoryCheck(party, gameMap)

        if result != "go":
            print(result)
            break
        legal = False


main()
