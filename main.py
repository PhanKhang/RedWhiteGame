#!/usr/bin/python3
import numpy
from move import Move
from validator import Validator
from appraiser import Appraiser
from placer import Placer
from cell import Cell
from treenode import Treenode
import copy

# game map
gameMap = numpy.zeros((12, 8))
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
    if i == 1 :
        return redB + dot
    if i == 2 :
        return whiteB + ring
    if i == 3 :
        return redB + ring
    if i == 4 :
        return whiteB + dot
    return " 0"


def getCardL(i):
    whiteB = "W"
    redB = "R"
    dot = "D"
    ring = "C"
    if i == 1 :
        return redB + dot
    if i == 2 :
        return whiteB + ring
    if i == 3 :
        return redB + ring
    if i == 4 :
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
        s = str(j+1)+"\t"
        for i in range(8):
            s += getCardL(gameMap[j][i])
            s += " "
            s += ENDC
        print(s, ENDC)
    print("     A  B  C  D  E  F  G  H")


def correctPrinterMap(gameMap):
    ENDC = '\033[2m'
    print("     A  B  C  D  E  F  G  H")
    for j in range(11, -1, -1):
        s = str(j+1)+"\t"
        for i in range(8):
            s += getCard(gameMap[j][i])
            s += " "
            s += ENDC
        print(s, ENDC)
    print("     A  B  C  D  E  F  G  H")


def alphabeta(node, depth, a, b, maxP):
    if depth == 0 or node.goalState != 'go':
        return node.weight
    if maxP:
        node.weight = -9999999
        newchildren = []
        for childnode in node.children:
            node.weight = max(node.weight, alphabeta(childnode, depth -1, a, b, False))
            a = max(a, node.weight)
            newchildren.append(childnode)
            if a >= b:
                #print("prune!")
                node.children = newchildren
                break
        return node.weight
    else:
        node.weight = 9999999
        newchildren = []
        for childnode in node.children:
            node.weight = min(node.weight, alphabeta(childnode, depth -1, a, b, True))
            b = min(b, node.weight)
            newchildren.append(childnode)
            if a >= b:
                #print("prune!")
                node.children = newchildren
                break
        return node.weight

valueMap = [[Cell() for j in range(8)] for i in range(12)]

def main():
    pruning = int(input("Activate alpha-beta pruning? 1 for yes 0 for no: "))
    trace = int(input("Generate trace? 1 for yes 0 for no: "))
    computer = int(input("Which player should be computer 1 or 2?: "))
    choice = int(input("Player 1  will be playing? 0 for dots and 1 a for colors: "))
    if choice == 0:
        print("Player 1: Dots")
        print("Player 2: Colors")
    else:
        print("Player 1: Colors")
        print("Player 2: Dots")
    legal = False

    Appraiser().setInitialValue(valueMap)
    party = 0
    for k in range(1, 61):
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

        while not legal:
            movok = False
            while not movok:
                newValueMap = copy.copy(valueMap)
                newGameMap = copy.copy(gameMap)
                input_var = ''
                if (k%2==1 and computer == 1) or (k%2 == 0 and computer == 2):
                    treenode = Treenode(4, newValueMap, newGameMap, k, validator, party, 0)
                    if pruning == 1:
                        alphabeta(treenode, 2,  -9999999, 9999999, True)
                    if treenode.getMove() == "0 7 F 2":
                        print("gotcha")
                    input_var = treenode.getMove()
                    print("computer move: " + input_var)
                else:
                    input_var = input()

                #print("Recommended move: " + treenode.getMove())
                # print(input_var)
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
        correctPrinterMap(gameMap) # change to correctPrinterMapL for letter output
        # print(validator.coordinateToRotation)
        appraiser.appraise(move, valueMap, gameMap)

        if (k + choice) % 2 == 0:
            print("Score for Colors: ")
            print(appraiser.getScoreColors())
        else:
            print("Score for Dots: ")
            print(appraiser.getScoreDots())

        tmp = {}
        print("Red map")
        # print(appraiser.getAvailableMoves(appraiser.getRedMap(), tmp))
        correctPrinter(appraiser.getRedMap(valueMap))

        print("White map")
        # print(appraiser.getAvailableMoves(appraiser.getWhiteMap(), tmp))
        correctPrinter(appraiser.getWhiteMap(valueMap))

        print("Ring map")
        # print(appraiser.getAvailableMoves(appraiser.getRingMap(), tmp))
        correctPrinter(appraiser.getRingMap(valueMap))

        print("Dot map")
        # print(appraiser.getAvailableMoves(appraiser.getDotMap(), tmp))
        correctPrinter(appraiser.getDotMap(valueMap))

        result = validator.victoryCheck((k + choice) % 2, gameMap)

        if result != "go":
            print(result)
            break
        legal = False


main()
