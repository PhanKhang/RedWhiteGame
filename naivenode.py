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
    def __init__(self, depth, level, gameMap, moveNum, validator, party, trace):
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

        def toPut(i, j):
            subCandidates = []
            if (i == 0 and gameMap[i][j] == 0) or (i < 11 and gameMap[i][j] == 0 and gameMap[i - 1][j] != 0):
                for position in [2, 6, 4, 8]:
                    subCandidates.append(
                        Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1)))
            if (i == 0 and j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0) or (
                    j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0 and gameMap[i - 1][j] != 0 and
                    gameMap[i - 1][j + 1] != 0):
                for position in [1, 3, 5, 7]:
                    subCandidates.append(
                        Candidate(str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1)))
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
                                int(i2) + 1))
            if (j < 7 and i < 11 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j] == 0 and
                gameMap[i + 1][j + 1] == 0) or (j < 7 and i == 11 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0):
                secondCardPart = validator.getCard(i, j)
                if secondCardPart != 'none':
                    i2 = secondCardPart.split(":")[0]
                    j2 = secondCardPart.split(":")[1]
                    if (i == i2) and (j + 1 == j2):
                        return Candidate(str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1) + str(
                            numbToLetter.get(int(j2))) + ' ' + str(int(i2) + 1))
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
                candidates.append(Candidate(move))

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
                            candidates.append(move)
            return candidates

        self.candidates = getCandidates()

        # krasnyCherny - 1
        # beluyKolco - 2
        # krasnyKolco - 3
        # beluyChernuy - 4

        # Naive heuristic implementation call here
        def getOwnWeight(gameMap):
            e = 0
            for i in range(8):
                for j in range(12):
                    if gameMap[j][i] == 2:
                        e += (j + 1) * 10 + (i + 1)
                    elif gameMap[j][i] == 4:
                        e += ((j + 1) * 10 + (i + 1)) * 3
                    elif gameMap[j][i] == 1:
                        e -= ((j + 1) * 10 + (i + 1)) * 2
                    elif gameMap[j][i] == 3:
                        e -= ((j + 1) * 10 + (i + 1)) * 1.5
            return e

        self.weight = getOwnWeight(self.gameMap)





        # here we detect if it's a goal state
        # would reuse victoryCheck, but need to refactor it a bit
        self.goalState = self.validator.victoryCheck(party, gameMap)

        if self.goalState == 'color wins' and party == 0:
            self.weight *= 10
        elif self.goalState == 'dots wins' and party == 1:
            self.weight *= 10

        def childcreator(moveString):
            move = Move(moveString)
            # print(moveString)
            if self.validator.placeValidator(move, gameMap):
                newGameMap = copy.copy(self.gameMap)
                newValidator = copy.copy(self.validator)
                Nonvalidatedplacer().place(move, newValidator, newGameMap)
                newparty = 0
                if self.party == 0:
                    newparty = 1
                if self.trace and self.level == 2:
                    self.eCalls += 1
                childNode = Naivenode(depth - 1, level + 1, newGameMap, moveNum + 1, newValidator, newparty,
                                      trace)
                childNode.rawMove = moveString
                self.children.append(childNode)

        def populateChildren(candidates):
            for candidate in candidates:
                childcreator(candidate.move)

        if self.depth > 0 and self.goalState == 'go':
            populateChildren(self.candidates)

    def getMove(self, weight):
        nextMove = self.children[0]
        for node in self.children:
            if nextMove.weight == weight:
                nextMove = node
        return nextMove.rawMove

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
                child.getL3value(level+1, weight)

    def getL2values(self):
        values = []
        for child in self.children:
            values.append(child.weight)
        return values

