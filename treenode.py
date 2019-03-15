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
    def __init__(self, depth, valueMap, gameMap, moveNum, validator, party, weightParent, width):
        self.depth = depth
        self.gameMap = gameMap
        self.valueMap = valueMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''
        self.coef = 0.8
        self.weightParent = weightParent
        self.goalState = "go"
        self.width = width
        self.weight = 0

        # self.goalState = self.validator.victoryCheck(party, gameMap)
        # if self.goalState == 'color wins' and party == 0:
        #     self.weight *= 10
        # elif self.goalState == 'dots wins' and party == 1:
        #     self.weight *= 10

    def getOwnWeight(self):
        self.weight = Appraiser().getScore(self.valueMap, self.gameMap)
        return self.weight

    def populateChildren(self):
        candidates = self.getCandidates()
        for candidate in candidates:
            self.childcreator(candidate.move)

    def getRecycleCandidateScore(self, i1, j1, i2, j2, party):
        score = 0
        if party == 0:
            score = max(self.valueMap[i1][j1].redWeight + self.valueMap[i2][j2].whiteWeight,
                        self.valueMap[i1][j1].whiteWeight + self.valueMap[i2][j2].redWeight)
        elif party == 1:
            score = max(self.valueMap[i1][j1].dotWeight + self.valueMap[i2][j2].ringWeight,
                        self.valueMap[i1][j1].ringWeight + self.valueMap[i2][j2].dotWeight)
        return score

    def getCandidateScore(self, i, j, position, party):
        score = 0
        if party == 0:
            if position in [1]:
                score = (self.valueMap[i][j].dotWeight + self.valueMap[i][j + 1].ringWeight) \
                        - (self.valueMap[i][j].redWeight + self.valueMap[i][j + 1].whiteWeight) * self.coef
            elif position in [2]:
                score = (self.valueMap[i][j].ringWeight + self.valueMap[i + 1][j].dotWeight) \
                        - (self.valueMap[i][j].whiteWeight + self.valueMap[i + 1][j].redWeight) * self.coef
            elif position in [3]:
                score = (self.valueMap[i][j].ringWeight + self.valueMap[i][j + 1].dotWeight) \
                        - (self.valueMap[i][j].whiteWeight + self.valueMap[i][j + 1].redWeight) * self.coef
            elif position in [4]:
                score = (self.valueMap[i][j].dotWeight + self.valueMap[i + 1][j].ringWeight) \
                        - (self.valueMap[i][j].redWeight + self.valueMap[i + 1][j].whiteWeight) * self.coef
            elif position in [5]:
                score = (self.valueMap[i][j].ringWeight + self.valueMap[i][j + 1].dotWeight) \
                        - (self.valueMap[i][j].redWeight + self.valueMap[i][j + 1].whiteWeight) * self.coef
            elif position in [6]:
                score = (self.valueMap[i][j].dotWeight + self.valueMap[i + 1][j].ringWeight) \
                        - (self.valueMap[i][j].whiteWeight + self.valueMap[i + 1][j].redWeight) * self.coef
            elif position in [7]:
                score = (self.valueMap[i][j].dotWeight + self.valueMap[i][j + 1].ringWeight) \
                        - (self.valueMap[i][j].whiteWeight + self.valueMap[i][j + 1].redWeight) * self.coef
            elif position in [8]:
                score = (self.valueMap[i][j].ringWeight + self.valueMap[i + 1][j].dotWeight) \
                        - (self.valueMap[i][j].redWeight + self.valueMap[i + 1][j].whiteWeight) * self.coef
        elif party == 1:
            if position in [1]:
                score = (self.valueMap[i][j].redWeight + self.valueMap[i][j + 1].whiteWeight) \
                        - (self.valueMap[i][j].dotWeight + self.valueMap[i][j + 1].ringWeight) * self.coef
            elif position in [2]:
                score = (self.valueMap[i][j].whiteWeight + self.valueMap[i + 1][j].redWeight) \
                        - (self.valueMap[i][j].ringWeight + self.valueMap[i + 1][j].dotWeight) * self.coef
            elif position in [3]:
                score = (self.valueMap[i][j].whiteWeight + self.valueMap[i][j + 1].redWeight) \
                        - (self.valueMap[i][j].ringWeight + self.valueMap[i][j + 1].dotWeight) * self.coef
            elif position in [4]:
                score = (self.valueMap[i][j].redWeight + self.valueMap[i + 1][j].whiteWeight) \
                        - (self.valueMap[i][j].dotWeight + self.valueMap[i + 1][j].ringWeight) * self.coef
            elif position in [5]:
                score = (self.valueMap[i][j].redWeight + self.valueMap[i][j + 1].whiteWeight) \
                        - (self.valueMap[i][j].ringWeight + self.valueMap[i][j + 1].dotWeight) * self.coef
            elif position in [6]:
                score = (self.valueMap[i][j].whiteWeight + self.valueMap[i + 1][j].redWeight) \
                        - (self.valueMap[i][j].dotWeight + self.valueMap[i + 1][j].ringWeight) * self.coef
            elif position in [7]:
                score = (self.valueMap[i][j].whiteWeight + self.valueMap[i][j + 1].redWeight) \
                        - (self.valueMap[i][j].dotWeight + self.valueMap[i][j + 1].ringWeight) * self.coef
            elif position in [8]:
                score = (self.valueMap[i][j].redWeight + self.valueMap[i + 1][j].whiteWeight) \
                        - (self.valueMap[i][j].ringWeight + self.valueMap[i + 1][j].dotWeight) * self.coef
        return score

    def toPut(self, i, j):
        subCandidates = []
        if (i == 0 and self.gameMap[i][j] == 0) or (i < 11 and self.gameMap[i][j] == 0 and self.gameMap[i - 1][j] != 0):
            for position in [2, 6, 4, 8]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1),
                              (self.getCandidateScore(i, j, position, self.party))))
        if (i == 0 and j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0) or (
                j < 7 and self.gameMap[i][j] == 0 and self.gameMap[i][j + 1] == 0 and self.gameMap[i - 1][j] != 0 and
                self.gameMap[i - 1][j + 1] != 0):
            for position in [1, 3, 5, 7]:
                subCandidates.append(
                    Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1),
                              (self.getCandidateScore(i, j, position, self.party))))
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
                            int(i2) + 1), self.getRecycleCandidateScore(i - 1, j, i2, j2, self.party))
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
                        numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1),
                                     self.getRecycleCandidateScore(i, j, i2, j2, self.party))
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
                score = putCandidate.score
                candidates.append(Candidate(move, score))
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
                        score = pickCandidate.score + putCandidate.score
                        candidates.append(move, score)

        candidates.sort(key=lambda x: x.score, reverse=True)
        if self.width != 0 & len(candidates) > self.width:
            return candidates[:self.width]
        return candidates

    def childcreator(self, moveString):
        move = Move(moveString)
        # print(moveString)
        if self.validator.placeValidator(move, self.gameMap):
            newGameMap = copy.copy(self.gameMap)
            newValueMap = copy.deepcopy(self.valueMap)
            newValidator = copy.copy(self.validator)

            Nonvalidatedplacer().place(move, newValidator, newGameMap)
            Appraiser().appraise(move, newValueMap, newGameMap)
            newparty = 0
            if self.party == 0:
                newparty = 1
            childNode = Treenode(self.depth - 1, newValueMap, newGameMap, self.moveNum + 1, newValidator, newparty,
                                 self.weight, self.width)
            childNode.rawMove = moveString
            self.children.append(childNode)

    def getMove(self, weight):
        for node in self.children:
            if node.weight == weight:
                return node.rawMove
