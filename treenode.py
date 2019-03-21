from move import Move
from appaiserNonValueMap import AppraiserNonValueMap
from nonvalidatedplacer import Nonvalidatedplacer
import copy
import numpy


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
    def __init__(self, move, score):
        self.move = move
        self.score = score


class Treenode:
    def __init__(self, depth, gameMap, moveNum, validator, party, width, coordinateToRotation):
        self.depth = depth
        self.gameMap = gameMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''
        self.coef = 0.8

        self.valueMapRed = numpy.zeros((12, 8))
        self.valueMapWhite = numpy.zeros((12, 8))
        self.valueMapDot = numpy.zeros((12, 8))
        self.valueMapRing = numpy.zeros((12, 8))



        self.width = width
        self.weight = 0
        self.lroot = ''
        self.coordinateToRotation = coordinateToRotation
        self.scoreColor = 0
        self.scoreDots = 0

        if self.depth > 0:
            self.goalState = AppraiserNonValueMap().appraise(self.gameMap, self)
        else:
            self.goalState = "go"

    # valueMapRed = numpy.zeros((12, 8))
    # valueMapWhite = numpy.zeros((12, 8))
    # valueMapDot = numpy.zeros((12, 8))
    # valueMapRing = numpy.zeros((12, 8))

        # self.goalState = self.validator.victoryCheck(party, gameMap)
        # if self.goalState == 'color wins' and party == 0:
        #     self.weight *= 10
        # elif self.goalState == 'dots wins' and party == 1:
        #     self.weight *= 10

    def getOwnWeight(self):
        self.goalState = AppraiserNonValueMap().appraise(self.gameMap, self)
        self.weight = AppraiserNonValueMap().getScore(self.party, self.goalState, self)
        return self.weight

    def populateChildren(self):
        candidates = self.getCandidates()
        for candidate in candidates:
            self.childcreator(candidate.move)
        if self.depth > 0:
            self.belovedChildren()

    def belovedChildren(self):
        if self.party == 0:
            self.children.sort(key=lambda x: x.scoreDots, reverse=True)
        else:
            self.children.sort(key=lambda x: x.scoreColor, reverse=True)
        if self.width != 0 and len(self.children) > self.width:
            self.children = self.children[:self.width]


    # def belovedChildren(self):
    #     if self.party == 0:
    #         self.children.sort(key=lambda x: x.scoreDots-x.scoreColor, reverse=True)
    #     else:
    #         self.children.sort(key=lambda x: x.scoreColor-x.scoreDots, reverse=True)
    #     if self.width != 0 and len(self.children) > self.width:
    #         self.children = self.children[:self.width]

    # def getRecycleCandidateScore(self, i1, j1, i2, j2, party):
    #     score = 0
    #     if party == 0:
    #         score = max(self.valueMapRed[i1][j1] + self.valueMapWhite[i2][j2],
    #                     self.valueMapWhite[i1][j1] + self.valueMapRed[i2][j2])
    #     elif party == 1:
    #         score = max(self.valueMapDot[i1][j1] + self.valueMapRing[i2][j2],
    #                     self.valueMapRing[i1][j1] + self.valueMapDot[i2][j2])
    #     return score
    #
    # def getCandidateScore(self, i, j, position, party):
    #     score = 0
    #     if party == 0:
    #         if position in [1]:
    #             score = (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) \
    #                     - (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) * self.coef
    #         elif position in [2]:
    #             score = (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) \
    #                     - (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) * self.coef
    #         elif position in [3]:
    #             score = (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) \
    #                     - (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) * self.coef
    #         elif position in [4]:
    #             score = (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) \
    #                     - (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) * self.coef
    #         elif position in [5]:
    #             score = (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) \
    #                     - (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) * self.coef
    #         elif position in [6]:
    #             score = (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) \
    #                     - (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) * self.coef
    #         elif position in [7]:
    #             score = (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) \
    #                     - (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) * self.coef
    #         elif position in [8]:
    #             score = (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) \
    #                     - (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) * self.coef
    #     elif party == 1:
    #         if position in [1]:
    #             score = (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) \
    #                     - (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) * self.coef
    #         elif position in [2]:
    #             score = (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) \
    #                     - (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) * self.coef
    #         elif position in [3]:
    #             score = (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) \
    #                     - (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) * self.coef
    #         elif position in [4]:
    #             score = (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) \
    #                     - (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) * self.coef
    #         elif position in [5]:
    #             score = (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) \
    #                     - (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) * self.coef
    #         elif position in [6]:
    #             score = (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) \
    #                     - (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) * self.coef
    #         elif position in [7]:
    #             score = (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) \
    #                     - (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) * self.coef
    #         elif position in [8]:
    #             score = (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) \
    #                     - (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) * self.coef
    #     return score

    def toPut(self, i, j, gameMap):
        subCandidates = []
        if (i == 0 and gameMap[i][j] == 0) or (i < 11 and gameMap[i][j] == 0 and gameMap[i - 1][j] != 0):
            for position in [2, 6, 4, 8]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), 0))
                # (self.getCandidateScore(i, j, position, self.party))))
        if (i == 0 and j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0) or (
                j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0 and gameMap[i - 1][j] != 0 and
                gameMap[i - 1][j + 1] != 0):
            for position in [1, 3, 5, 7]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), 0))
                # (self.getCandidateScore(i, j, position, self.party))))
        return subCandidates

    def toPick(self, i, j, coordinateToRotation):
        if (11 > i > 0 != self.gameMap[i - 1][j] and self.gameMap[i][j] != 0 and self.gameMap[i + 1][j] == 0) or (
                i == 11 and self.gameMap[i][j] != 0 and self.gameMap[i - 1][j] != 0):
            secondCardPart = self.validator.getCard(i - 1, j, coordinateToRotation)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if i == int(i2) and j == int(j2):
                    return Candidate(
                        str(numbToLetter.get(int(j))) + ' ' + str(i) + ' ' + str(numbToLetter.get(int(j2))) + ' '
                        + str(int(i2) + 1), 0)  # self.getRecycleCandidateScore(i - 1, j, i2, j2, self.party))
        if (j < 7 and i < 11 and self.gameMap[i][j] != 0 and self.gameMap[i][j + 1] != 0 and self.gameMap[i + 1][
            j] == 0 and
            self.gameMap[i + 1][j + 1] == 0) or (
                j < 7 and i == 11 and self.gameMap[i][j] != 0 and self.gameMap[i][j + 1] != 0):
            secondCardPart = self.validator.getCard(i, j, coordinateToRotation)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if (i == int(i2)) and (j + 1 == int(j2)):
                    return Candidate(str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1) + ' ' + str(
                        numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1), 0)
                    # self.getRecycleCandidateScore(i, j, i2, j2, self.party))
        return 'none'

    def getPutCandidates(self, gameMap):
        size = 0
        putCandidates = []
        for i in range(12):
            for j in range(8):
                putCandidate = self.toPut(i, j, gameMap)
                if putCandidate != 'none':
                    putCandidates += putCandidate
                    size += 1
                if size == 15:
                    break
        return putCandidates

    def getCandidates(self):
        candidates = []
        pickCandidates = []
        if self.moveNum <= 24:
            putCandidates = self.getPutCandidates(self.gameMap)
            for putCandidate in putCandidates:
                move = '0 ' + putCandidate.move
                candidates.append(Candidate(move, 0))
        else:
            size = 0
            for i in range(12):
                for j in range(8):
                    pickCandidate = self.toPick(i, j, self.coordinateToRotation)
                    if pickCandidate != 'none':
                        i1 = int(pickCandidate.move.split(" ")[1])
                        j1 = int(self.validator.letterToNumb.get(pickCandidate.move.split(" ")[0]))
                        if not (
                                j1 == self.validator.lastMove.targetCoordinateLet and i1 == self.validator.lastMove.targetCoordinateNum):
                            pickCandidates.append(pickCandidate)
                            size += 1
                    if size == 8:
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
                        candidates.append(Candidate(move, 0))

        # candidates.sort(key=lambda x: x.score, reverse=True)
        # if self.width != 0 & len(candidates) > self.width:
        #   return candidates[:self.width]
        return candidates

    def childcreator(self, moveString):
        move = Move(moveString)
        # print(moveString)
        if self.validator.placeValidator(move, self.gameMap):
            newGameMap = copy.copy(self.gameMap)
            # newvalueMapRed = copy.copy(self.valueMapRed)
            # newvalueMapWhite = copy.copy(self.valueMapWhite)
            # newvalueMapRing = copy.copy(self.valueMapRing)
            # newvalueMapDot = copy.copy(self.valueMapDot)
            newValidator = copy.copy(self.validator)
            newcoordinateToRotation = copy.copy(self.coordinateToRotation)

            newparty = 0
            if self.party == 0:
                newparty = 1

            Nonvalidatedplacer().place(move, newValidator, newGameMap, newcoordinateToRotation)

            childNode = Treenode(self.depth - 1,
                                 newGameMap, self.moveNum + 1, newValidator, newparty, self.width,
                                 newcoordinateToRotation)

            childNode.rawMove = moveString
            self.children.append(childNode)

    def setLroot(self):
        maxVal = 0
        if self.party == 0:
            for j in range(12):
                for i in range(8):
                    if self.valueMapRing[j][i] > maxVal:
                        maxVal = self.valueMapRing[j][i]
                        self.lroot = self.validator.numbToLetter.get(i + 1)
                    if self.valueMapDot[j][i] > maxVal:
                        maxVal = self.valueMapDot[j][i]
                        self.lroot = self.validator.numbToLetter.get(i + 1)
        if self.party == 1:
            for j in range(12):
                for i in range(8):
                    if self.valueMapRed[j][i] > maxVal:
                        maxVal = self.valueMapRed[j][i]
                        self.lroot = self.validator.numbToLetter.get(i + 1)
                    if self.valueMapWhite[j][i] > maxVal:
                        maxVal = self.valueMapWhite[j][i]
                        self.lroot = self.validator.numbToLetter.get(i + 1)

    def distance(self, treenode):
        nroot = ord(self.lroot)
        nnum = ord(treenode.rawMove[-3:-2])
        return abs(nroot - nnum)

    def getMove(self, weight):
        move = ""
        count = 0
        self.setLroot()
        self.children.sort(key=self.distance, reverse=False)
        for node in self.children:
            # print(node.rawMove + "____"+ str(node.weight))
            if node.weight == weight:
                # move = node.rawMove
                # print(move)
                # count += 1
                return node.rawMove
        # print("_______"+str(weight)+"_______")
        # print(count)
        # return move
