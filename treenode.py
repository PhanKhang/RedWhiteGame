from validator import Validator
from move import Move
from placer import Placer
from appraiser import Appraiser
import copy
from nonvalidatedplacer import  Nonvalidatedplacer
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
    def __init__(self, depth, level, valueMap, gameMap, moveNum, validator, party, trace):
        self.depth = depth
        self.level = level
        self.gameMap = gameMap
        self.valueMap = valueMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''
        self.coef = 0.8
        self.trace = trace
        self.eCalls = 0

        def getRecycleCandidateScore(i1, j1, i2, j2, party):
            score = 0
            if party == 0:
                score = max(valueMap[i1][j1].redWeight + valueMap[i2][j2].whiteWeight, valueMap[i1][j1].whiteWeight + valueMap[i2][j2].redWeight)
            elif party == 1:
                score = max(valueMap[i1][j1].dotWeight + valueMap[i2][j2].ringWeight, valueMap[i1][j1].ringWeight + valueMap[i2][j2].dotWeight)
            return score

        def getCandidateScore(i, j, position, party):
            score = 0
            if party == 0:
                if position in [1]:
                    score = (valueMap[i][j].dotWeight + valueMap[i][j + 1].ringWeight) \
                            - (valueMap[i][j].redWeight + valueMap[i][j + 1].whiteWeight) * self.coef
                elif position in [2]:
                    score = (valueMap[i][j].ringWeight + valueMap[i + 1][j].dotWeight) \
                            - (valueMap[i][j].whiteWeight + valueMap[i + 1][j].redWeight) * self.coef
                elif position in [3]:
                    score = (valueMap[i][j].ringWeight + valueMap[i][j + 1].dotWeight) \
                            - (valueMap[i][j].whiteWeight + valueMap[i][j + 1].redWeight) * self.coef
                elif position in [4]:
                    score = (valueMap[i][j].dotWeight + valueMap[i + 1][j].ringWeight) \
                            - (valueMap[i][j].redWeight + valueMap[i + 1][j].whiteWeight) * self.coef
                elif position in [5]:
                    score = (valueMap[i][j].ringWeight + valueMap[i][j + 1].dotWeight) \
                            - (valueMap[i][j].redWeight + valueMap[i][j + 1].whiteWeight) * self.coef
                elif position in [6]:
                    score = (valueMap[i][j].dotWeight + valueMap[i + 1][j].ringWeight) \
                            - (valueMap[i][j].whiteWeight + valueMap[i + 1][j].redWeight) * self.coef
                elif position in [7]:
                    score = (valueMap[i][j].dotWeight + valueMap[i][j + 1].ringWeight) \
                            - (valueMap[i][j].whiteWeight + valueMap[i][j + 1].redWeight) * self.coef
                elif position in [8]:
                    score = (valueMap[i][j].ringWeight + valueMap[i + 1][j].dotWeight) \
                            - (valueMap[i][j].redWeight + valueMap[i + 1][j].whiteWeight) * self.coef
            elif party == 1:
                if position in [1]:
                    score = (valueMap[i][j].redWeight + valueMap[i][j + 1].whiteWeight) \
                            - (valueMap[i][j].dotWeight + valueMap[i][j + 1].ringWeight) * self.coef
                elif position in [2]:
                    score = (valueMap[i][j].whiteWeight + valueMap[i + 1][j].redWeight) \
                            - (valueMap[i][j].ringWeight + valueMap[i + 1][j].dotWeight) * self.coef
                elif position in [3]:
                    score = (valueMap[i][j].whiteWeight + valueMap[i][j + 1].redWeight) \
                            - (valueMap[i][j].ringWeight + valueMap[i][j + 1].dotWeight) * self.coef
                elif position in [4]:
                    score = (valueMap[i][j].redWeight + valueMap[i + 1][j].whiteWeight) \
                            - (valueMap[i][j].dotWeight + valueMap[i + 1][j].ringWeight) * self.coef
                elif position in [5]:
                    score = (valueMap[i][j].redWeight + valueMap[i][j + 1].whiteWeight) \
                            - (valueMap[i][j].ringWeight + valueMap[i][j + 1].dotWeight) * self.coef
                elif position in [6]:
                    score = (valueMap[i][j].whiteWeight + valueMap[i + 1][j].redWeight) \
                            - (valueMap[i][j].dotWeight + valueMap[i + 1][j].ringWeight) * self.coef
                elif position in [7]:
                    score = (valueMap[i][j].whiteWeight + valueMap[i][j + 1].redWeight) \
                            - (valueMap[i][j].dotWeight + valueMap[i][j + 1].ringWeight) * self.coef
                elif position in [8]:
                    score = (valueMap[i][j].redWeight + valueMap[i + 1][j].whiteWeight) \
                            - (valueMap[i][j].ringWeight + valueMap[i + 1][j].dotWeight) * self.coef
            # return Candidate('0 ' + str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), score)
            return score

        def toPut(i, j):
            subCandidates = []
            if (i == 0 and gameMap[i][j] == 0) or (i < 11 and gameMap[i][j] == 0 and gameMap[i - 1][j] != 0):
                for position in [2, 6, 4, 8]:
                    subCandidates.append(Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1),
                                     (getCandidateScore(i, j, position, party))))
            if (i == 0 and j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0) or (
                    j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0 and gameMap[i - 1][j] != 0 and
                    gameMap[i - 1][j + 1] != 0):
                for position in [1, 3, 5, 7]:
                    subCandidates.append(Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1),
                                     (getCandidateScore(i, j, position, party))))
            return subCandidates

        def toPick(i, j):
            if (0 < i < 11 and gameMap[i][j] != 0 and gameMap[i - 1][j] != 0 and gameMap[i + 1][j] == 0) or (
                    i == 11 and gameMap[i][j] != 0 and gameMap[i - 1][j] != 0):
                secondCardPart = validator.getCard(i - 1, j)
                if secondCardPart != 'none':
                    i2 = secondCardPart.split(":")[0]
                    j2 = secondCardPart.split(":")[1]
                    if (i == i2 and j == j2):
                        return Candidate(
                            str(numbToLetter.get(int(j))) + ' ' + str(i) + str(numbToLetter.get(int(j2))) + ' ' + str(
                                int(i2) + 1), getRecycleCandidateScore(i - 1, j, i2, j2, party))
            if (j < 7 and i < 11 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j] == 0 and
                gameMap[i + 1][j + 1] == 0) or (j < 7 and i == 11 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0):
                secondCardPart = validator.getCard(i, j)
                if secondCardPart != 'none':
                    i2 = secondCardPart.split(":")[0]
                    j2 = secondCardPart.split(":")[1]
                    if (i == i2) and (j + 1 == j2):
                        return Candidate(str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1) + str(
                            numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1),
                                         getRecycleCandidateScore(i, j, i2, j2, party))
            return 'none'

        def getCandidates():
            candidates = []
            putCandidates = []
            pickCandidates = []
            size = 0
            for i in range(12):
                for j in range(8):
                    putCandidate = toPut(i, j)
                    if putCandidate != 'none':
                        putCandidates += putCandidate
                        size += 1
                    if size == 14:
                        break

            for putCandidate in putCandidates:
                move = '0 ' + putCandidate.move
                score = putCandidate.score
                candidates.append(Candidate(move, score))

            if moveNum > 24:
                size = 0
                for i in range(12):
                    for j in range(8):
                        pickCandidate = toPick(i, j)
                        if pickCandidate != 'none':
                            pickCandidates.append(pickCandidate)
                            size += 1
                        if size == 7:
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
            if len(candidates) > 5:
                return candidates[:5]
            return candidates

        self.candidates = getCandidates()

        # here we place move heuristic weight (as discussed OUR MAX- ENEMY MAX)
        # which represents h()
        def getOwnWeight(valueMap):
            if party == 0:  # maybe 1 stays for dots?
                return Appraiser().getScoreColors()
            else:
                return Appraiser().getScoreDots()

        self.goalState = self.validator.victoryCheck(party, gameMap)
        self.weight = getOwnWeight(self.valueMap)


        if self.goalState == 'color wins' and party == 0:
            self.weight *= 10
        elif self.goalState == 'dots wins' and party == 1:
            self.weight *= 10


        # here we detect if it's a goal state
        # would reuse victoryCheck, but need to refactor it a bit

        def childcreator(moveString):
            move = Move(moveString)
            # print(moveString)
            if self.validator.placeValidator(move, gameMap):
                newGameMap = copy.copy(self.gameMap)
                newValueMap = copy.deepcopy(self.valueMap)
                newValidator = copy.copy(self.validator)

                Nonvalidatedplacer().place(move, newValidator, newGameMap)
                Appraiser().appraise(move, newValueMap, newGameMap)
                newparty = 0
                if self.party == 0:
                    newparty = 1

                if self.trace and self.level == 2:
                    self.eCalls +=1
                childNode = Treenode(depth - 1, level + 1, newValueMap, newGameMap, moveNum + 1, newValidator, newparty, trace)
                childNode.rawMove = moveString
                self.children.append(childNode)

        def populateChildren(candidates):
            for candidate in candidates:
                childcreator(candidate.move)

        if self.depth > 0 and self.goalState == 'go':
            populateChildren(self.candidates)

        if self.trace and self.level == 2:
            open("trace.txt", "a").write(self.eCalls)


    def getMove(self, weight):
        nextMove = self.children[0]
        for node in self.children:
            if nextMove.weight == weight:
                nextMove = node
        return nextMove.rawMove
