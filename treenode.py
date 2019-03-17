from validator import Validator
from move import Move
from placer import Placer
from appraiser import Appraiser
import copy
from nonvalidatedplacer import Nonvalidatedplacer
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
    def __init__(self, depth, valueMapRed, valueMapWhite, valueMapRing, valueMapDot, gameMap, moveNum, validator, party, width, goalState):
        self.depth = depth
        self.gameMap = gameMap

        self.valueMapRed = valueMapRed
        self.valueMapRing = valueMapRing
        self.valueMapDot = valueMapDot
        self.valueMapWhite = valueMapWhite

        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''
        self.coef = 0.8
        self.goalState = goalState
        self.width = width
        self.weight = 0

        # self.goalState = self.validator.victoryCheck(party, gameMap)
        # if self.goalState == 'color wins' and party == 0:
        #     self.weight *= 10
        # elif self.goalState == 'dots wins' and party == 1:
        #     self.weight *= 10

    def getOwnWeight(self):
        self.weight = Appraiser().getScore(self.valueMapRed, self.valueMapWhite, self.valueMapRing, self.valueMapDot, self.party)
        return self.weight

    def populateChildren(self):
        candidates = self.getCandidates()
        for candidate in candidates:
            self.childcreator(candidate.move)

    def getRecycleCandidateScore(self, i1, j1, i2, j2, party):
        score = 0
        if party == 0:
            score = max(self.valueMapRed[i1][j1] + self.valueMapWhite[i2][j2],
                        self.valueMapWhite[i1][j1] + self.valueMapRed[i2][j2])
        elif party == 1:
            score = max(self.valueMapDot[i1][j1] + self.valueMapRing[i2][j2],
                        self.valueMapRing[i1][j1] + self.valueMapDot[i2][j2])
        return score

    def getCandidateScore(self, i, j, position, party):
        score = 0
        if party == 0:
            if position in [1]:
                score = (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) \
                        - (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) * self.coef
            elif position in [2]:
                score = (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) \
                        - (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) * self.coef
            elif position in [3]:
                score = (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) \
                        - (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) * self.coef
            elif position in [4]:
                score = (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) \
                        - (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) * self.coef
            elif position in [5]:
                score = (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) \
                        - (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) * self.coef
            elif position in [6]:
                score = (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) \
                        - (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) * self.coef
            elif position in [7]:
                score = (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) \
                        - (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) * self.coef
            elif position in [8]:
                score = (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) \
                        - (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) * self.coef
        elif party == 1:
            if position in [1]:
                score = (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) \
                        - (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) * self.coef
            elif position in [2]:
                score = (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) \
                        - (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) * self.coef
            elif position in [3]:
                score = (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) \
                        - (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) * self.coef
            elif position in [4]:
                score = (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) \
                        - (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) * self.coef
            elif position in [5]:
                score = (self.valueMapRed[i][j] + self.valueMapWhite[i][j + 1]) \
                        - (self.valueMapRing[i][j] + self.valueMapDot[i][j + 1]) * self.coef
            elif position in [6]:
                score = (self.valueMapWhite[i][j] + self.valueMapRed[i + 1][j]) \
                        - (self.valueMapDot[i][j] + self.valueMapRing[i + 1][j]) * self.coef
            elif position in [7]:
                score = (self.valueMapWhite[i][j] + self.valueMapRed[i][j + 1]) \
                        - (self.valueMapDot[i][j] + self.valueMapRing[i][j + 1]) * self.coef
            elif position in [8]:
                score = (self.valueMapRed[i][j] + self.valueMapWhite[i + 1][j]) \
                        - (self.valueMapRing[i][j] + self.valueMapDot[i + 1][j]) * self.coef
        return score

    def toPut(self, i, j):
        subCandidates = []
        if (i == 0 and self.gameMap[i][j] == 0) or (i < 11 and self.gameMap[i][j] == 0 and self.gameMap[i - 1][j] != 0):
            for position in [2, 6, 4, 8]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), 0))
                              #(self.getCandidateScore(i, j, position, self.party))))
        if (i == 0 and j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0) or (
                j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0 and self.gameMap[i - 1][j] != 0 and
                self.gameMap[i - 1][j + 1] != 0):
            for position in [1, 3, 5, 7]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), 0))
                              #(self.getCandidateScore(i, j, position, self.party))))
        return subCandidates

    def toPick(self, i, j):
        if (0 < i < 11 and self.gameMap[i][j] != 0 and self.gameMap[i - 1][j] != 0 and self.gameMap[i + 1][j] == 0) or (
                i == 11 and self.gameMap[i][j] != 0 and self.gameMap[i - 1][j] != 0):
            secondCardPart = self.validator.getCard(i - 1, j)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if (i == i2 and j == j2):
                    return Candidate(
                        str(numbToLetter.get(int(j))) + ' ' + str(i) + str(numbToLetter.get(int(j2))) + ' ' + str(
                            int(i2) + 1), 0)#self.getRecycleCandidateScore(i - 1, j, i2, j2, self.party))
        if (j < 7 and i < 11 and self.gameMap[i][j] != 0 and self.gameMap[i][j + 1] != 0 and self.gameMap[i + 1][
            j] == 0 and
            self.gameMap[i + 1][j + 1] == 0) or (
                j < 7 and i == 11 and self.gameMap[i][j] != 0 and self.gameMap[i][j + 1] != 0):
            secondCardPart = self.validator.getCard(i, j)
            if secondCardPart != 'none':
                i2 = secondCardPart.split(":")[0]
                j2 = secondCardPart.split(":")[1]
                if (i == i2) and (j + 1 == j2):
                    return Candidate(str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1) + str(
                        numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1),0)
                                     #self.getRecycleCandidateScore(i, j, i2, j2, self.party))
        return 'none'

    def getCandidates(self):
        candidates = []
        putCandidates = []
        pickCandidates = []
        if self.moveNum <= 24:
            size = 0
            for i in range(12):
                for j in range(8):
                    putCandidate = self.toPut(i, j)
                    if putCandidate != 'none':
                        putCandidates += putCandidate
                        size += 1
                    if size == 15:
                        break

            for putCandidate in putCandidates:
                move = '0 ' + putCandidate.move
                #score = putCandidate.score
                candidates.append(Candidate(move, 0))
        else:
            size = 0
            for i in range(12):
                for j in range(8):
                    pickCandidate = self.toPick(i, j)
                    if pickCandidate != 'none':
                        pickCandidates.append(pickCandidate)
                        size += 1
                    if size == 8:
                        break
            for pickCandidate in pickCandidates:
                for putCandidate in putCandidates:
                    if (putCandidate.move.split(" ")[1] != pickCandidate.move.split(" ")[0] and
                        putCandidate.move.split(" ")[2] != pickCandidate.move.split(" ")[1]) \
                            or (putCandidate.move.split(" ")[1] != pickCandidate.move.split(" ")[2] and
                                putCandidate.move.split(" ")[2] != pickCandidate.move.split(" ")[3]):
                        move = pickCandidate.move + ' ' + putCandidate.move
                        #score = pickCandidate.score + putCandidate.score
                        candidates.append(move, 0)

        #candidates.sort(key=lambda x: x.score, reverse=True)
        #if self.width != 0 & len(candidates) > self.width:
        #   return candidates[:self.width]
        return candidates

    def childcreator(self, moveString):
        move = Move(moveString)
        # print(moveString)
        if self.validator.placeValidator(move, self.gameMap):
            newGameMap = copy.copy(self.gameMap)
            newvalueMapRed = copy.copy(self.valueMapRed)
            newvalueMapWhite = copy.copy(self.valueMapWhite)
            newvalueMapRing = copy.copy(self.valueMapRing)
            newvalueMapDot = copy.copy(self.valueMapDot)
            newValidator = copy.copy(self.validator)

            Nonvalidatedplacer().place(move, newValidator, newGameMap)
            result = Appraiser().appraise(move, newvalueMapRed, newvalueMapWhite, newvalueMapRing, newvalueMapDot, newGameMap)


            goalState = "go"
            if result:
                print("I won")
                goalState = "win"

            newparty = 0
            if self.party == 0:
                newparty = 1
            childNode = Treenode(self.depth - 1, newvalueMapRed, newvalueMapWhite, newvalueMapRing, newvalueMapDot, newGameMap, self.moveNum + 1, newValidator, newparty, self.width, goalState)
            childNode.rawMove = moveString
            self.children.append(childNode)

    def getMove(self, weight):
        move = ""
        count = 0
        for node in self.children:
            print(node.rawMove + "____"+ str(node.weight))
            if node.weight == weight:
                move = node.rawMove
                # print(move)
                count += 1
                # return node.rawMove
        print("_______"+str(weight)+"_______")
        print(count)
        return move