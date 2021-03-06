from move import Move
import copy
from nonvalidatedplacer import Nonvalidatedplacer

numbToLetter = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H"
}


class Candidate:
    def __init__(self, move):
        self.move = move


class Naivenode:
    def __init__(self, depth, level, gameMap, moveNum, validator, party, trace, parent, coordinateToRotation):
        self.depth = depth
        self.level = level
        self.gameMap = gameMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''
        self.trace = trace
        self.eCalls = 0
        self.parent = parent
        self.coordinateToRotation = coordinateToRotation
        self.candidates = []

        # krasnyCherny - 1
        # beluyKolco - 2
        # krasnyKolco - 3
        # beluyChernuy - 4

        # Naive heuristic implementation call here

        self.weight = 0
        # here we detect if it's a goal state
        # would reuse victoryCheck, but need to refactor it a bit
        # self.goalState = self.validator.victoryCheck(party, gameMap)
        self.goalState = "go"

        # if self.goalState == 'color wins' and party == 0:
        #     self.weight *= 10
        # elif self.goalState == 'dots wins' and party == 1:
        #     self.weight *= 10

    def toPut(self, i, j, gameMap):
        subCandidates = []
        if (i == 0 and self.gameMap[i][j] == 0) or (i < 11 and self.gameMap[i][j] == 0 and self.gameMap[i - 1][j] != 0):
            for position in [2, 6, 4, 8]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1)))
        if (i == 0 and j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0) \
                or (j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0
                    and self.gameMap[i - 1][j] != 0 and self.gameMap[i - 1][j + 1] != 0):
            for position in [1, 3, 5, 7]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1)))
        return subCandidates

    def toPick(self, i, j):  # vertical pick
        if (0 < i < 11 and self.gameMap[i][j] != 0 and self.gameMap[i - 1][j] != 0 and self.gameMap[i + 1][j] == 0) or (
                i == 11 and self.gameMap[i][j] != 0 and self.gameMap[i - 1][j] != 0):
            secondCardPart = self.validator.getCard(i - 1, j, self.coordinateToRotation)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if (i == int(i2) and j == int(j2)):
                    return Candidate(
                        str(numbToLetter.get(int(j))) + ' ' + str(i) + ' ' + str(numbToLetter.get(int(j2))) + ' '
                        + str(int(i2) + 1))
        if (0 <= j < 7 and 0 <= i < 11 and self.gameMap[i][j] != 0 and self.gameMap[i][j + 1] != 0 and self.gameMap[i + 1][
            j] == 0 and self.gameMap[i + 1][j + 1] == 0) or (j < 7 and i == 11 and self.gameMap[i][j] != 0
                                                        and self.gameMap[i][j + 1] != 0):
            secondCardPart = self.validator.getCard(i, j, self.coordinateToRotation)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if (i == int(i2)) and (j + 1 == int(j2)):
                    return Candidate(str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1) + ' ' + str(
                        numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1))
        return 'none'


    def getPutCandidates(self, gameMap):
        size = 0
        putCandidates = []
        for i in range(12):
            for j in range(8):
                putCandidate = self.toPut(i, j, self.gameMap)
                if putCandidate != 'none':
                    putCandidates += putCandidate
                    size += 1
                # if size == 14:
                #     break
        return putCandidates


    def getCandidates(self):
        candidates = []
        pickCandidates = []
        putCandidates = []

        if self.moveNum <= 24:
            putCandidates = self.getPutCandidates(self.gameMap)
            for putCandidate in putCandidates:
                move = '0 ' + putCandidate.move
                candidates.append(Candidate(move))
        else:
            size = 0
            for i in range(12):
                for j in range(8):
                    pickCandidate = self.toPick(i, j)
                    if pickCandidate != 'none':
                        i1 = int(pickCandidate.move.split(" ")[1])
                        j1 = int(self.validator.letterToNumb.get(pickCandidate.move.split(" ")[0]))
                        if not (
                                j1 == self.validator.lastMove.targetCoordinateLet and i1 == self.validator.lastMove.targetCoordinateNum):
                            pickCandidates.append(pickCandidate)
                            size += 1
                    if size == 7:
                        break
            for pickCandidate in pickCandidates:
                pickGameMap = copy.copy(self.gameMap)
                i1 = int(pickCandidate.move.split(" ")[1])
                j1 = int(self.validator.letterToNumb.get(pickCandidate.move.split(" ")[0]))
                i2 = int(pickCandidate.move.split(" ")[3])
                j2 = int(self.validator.letterToNumb.get(pickCandidate.move.split(" ")[2]))
                pickGameMap[i1 - 1][j1 - 1] = 0
                pickGameMap[i2 - 1][j2 - 1] = 0
                pickPutCandidates = self.getPutCandidates(pickGameMap)
                for putCandidate in pickPutCandidates:
                    if not (int(self.coordinateToRotation.get(numbToLetter.get(j1 - 1) + str(i1))) == int(
                            putCandidate.move.split(" ")[0]) and pickCandidate.move.split(" ")[0] ==
                            putCandidate.move.split(" ")[1] and pickCandidate.move.split(" ")[1] ==
                            putCandidate.move.split(" ")[2]):
                        move = pickCandidate.move + ' ' + putCandidate.move
                        candidates.append(Candidate(move))
        return candidates


    def childcreator(self, moveString):
        move = Move(moveString)
        if self.validator.validateMove(move, self.gameMap, self.coordinateToRotation):
            newGameMap = copy.copy(self.gameMap)
            newValidator = copy.copy(self.validator)
            newCoordinateToRotation = copy.copy(self.coordinateToRotation)
            Nonvalidatedplacer().place(move, newValidator, newGameMap, newCoordinateToRotation)
            newparty = 0
            if self.party == 0:
                newparty = 1
            childNode = Naivenode(self.depth - 1, self.level + 1, newGameMap, self.moveNum + 1, newValidator, newparty,
                                  self.trace, self, newCoordinateToRotation)
            childNode.rawMove = moveString
            self.children.append(childNode)

    def populateChildren(self):
        self.candidates = self.getCandidates()
        for candidate in self.candidates:
            self.childcreator(candidate.move)

    def getOwnWeight(self):
        e = 0
        if self.trace and self.level == 3:
            self.parent.eCalls += 1
        for i in range(8):
            for j in range(12):
                if self.gameMap[j][i] == 2:
                    e += (j + 1) * 10 + (i + 1)
                elif self.gameMap[j][i] == 4:
                    e += ((j + 1) * 10 + (i + 1)) * 3
                elif self.gameMap[j][i] == 1:
                    e -= ((j + 1) * 10 + (i + 1)) * 2
                elif self.gameMap[j][i] == 3:
                    e -= ((j + 1) * 10 + (i + 1)) * 1.5
        self.weight = e
        return self.weight

    def getMove(self, weight):
        for node in self.children:
            if node.weight == weight:
                return node.rawMove

    def getECalls(self):
        result = 0
        for child in self.children:
            result += child.eCalls
        return result

    def getL3value(self, level, weight):
        for child in self.children:
            if child.weight == weight:
                if level == 2:
                    return child.weight
                else:
                    return child.getL3value(level + 1, weight)

    def getL2values(self):
        values = []
        for child in self.children:
            values.append(child.weight)
        return values
