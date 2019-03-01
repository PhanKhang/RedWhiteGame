from validator import Validator
from move import Move
from placer import Placer
from appraiser import Appraiser
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


# types = {
#     1:
#     2:
#     3:
#     4:
#     5:
#     6:
#     7:
#     8:
# }


class Candidate:
    def __init__(self, move, score):
        self.move = move
        self.score = score


class Treenode:
    def __init__(self, depth, valueMap, gameMap, moveNum, validator, party):
        self.depth = depth
        self.gameMap = gameMap
        self.valueMap = valueMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party
        self.rawMove = ''

        def getCandidateScore(i, j, position, party):
            score = 0
            if party == 0:
                if position in [1, 7]:
                    score = max(valueMap[i][j].dotWeight, valueMap[i][j + 1].ringWeight) - \
                            max(valueMap[i][j].whiteWeight, valueMap[i][j].redWeight,
                                valueMap[i][j + 1].whiteWeight, valueMap[i][j + 1].redWeight)
                elif position in [3, 5]:
                    score = max(valueMap[i][j].ringWeight, valueMap[i][j + 1].dotWeight) - \
                            max(valueMap[i][j].whiteWeight, valueMap[i][j].redWeight,
                                valueMap[i][j + 1].whiteWeight, valueMap[i][j + 1].redWeight)
                elif position in [2, 8]:
                    score = max(valueMap[i][j].ringWeight, valueMap[i+1][j].dotWeight) - \
                            max(valueMap[i][j].whiteWeight, valueMap[i][j].redWeight,
                                valueMap[i + 1][j].whiteWeight, valueMap[i + 1][j].redWeight)
                elif position in [4, 6]:
                    score = max(valueMap[i][j].dotWeight, valueMap[i + 1][j].ringWeight) - \
                            max(valueMap[i][j].whiteWeight, valueMap[i][j].redWeight,
                                valueMap[i + 1][j].whiteWeight, valueMap[i + 1][j].redWeight)
            elif party == 1:
                if position in [1, 5]:
                    score = max(valueMap[i][j].redWeight, valueMap[i][j + 1].whiteWeight) - \
                            max(valueMap[i][j].dotWeight, valueMap[i][j].ringWeight,
                                valueMap[i][j + 1].dotWeight, valueMap[i][j + 1].ringWeight)
                elif position in [3, 7]:
                    score = max(valueMap[i][j].whiteWeight, valueMap[i][j + 1].redWeight) - \
                            max(valueMap[i][j].dotWeight, valueMap[i][j].ringWeight,
                                valueMap[i][j + 1].dotWeight, valueMap[i][j + 1].ringWeight)
                elif position in [2, 6]:
                    score = max(valueMap[i][j].whiteWeight, valueMap[i + 1][j].redWeight) - \
                            max(valueMap[i][j].dotWeight, valueMap[i][j].ringWeight,
                                valueMap[i + 1][j].dotWeight, valueMap[i + 1][j].ringWeight)
                elif position in [4, 8]:
                    score = max(valueMap[i][j].redWeight, valueMap[i + 1][j].whiteWeight) - \
                            max(valueMap[i][j].dotWeight, valueMap[i][j].ringWeight,
                                valueMap[i + 1][j].dotWeight, valueMap[i + 1][j].ringWeight)
            return Candidate('0 ' + str(position) + ' ' + str(numbToLetter.get(int(j))) + ' ' + str(int(i) + 1), score)

        def getCandidates():
            candidates = []
            for i in range(12):
                for j in range(8):
                    if (i == 0 and gameMap[i][j] == 0) or (i < 11 and gameMap[i][j] == 0 and gameMap[i - 1][j] != 0):
                        for position in [2, 6, 4, 8]:
                            candidates.append(getCandidateScore(i, j, position, party))
                    if (i == 0 and j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0) or (
                            j < 7 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0 and gameMap[i - 1][j] != 0 and
                            gameMap[i - 1][j + 1] != 0):
                        for position in [1, 3, 5, 7]:
                            newparty = 0
                            if party == 0:
                                newparty = 1
                            candidates.append(getCandidateScore(i, j, position, newparty))
            candidates.sort(key=lambda x: x.score, reverse=True)
            if len(candidates) > 5:
                return candidates[:5]
            return candidates

        self.candidates = getCandidates()

        # def getVerticalTargets(gameMap, valueMap, type):
        #     result = []
        #     size = 0
        #     for i in range(11):
        #         for j in range(8):
        #             if (i == 0 and gameMap[i][j] == 0) or (gameMap[i][j] == 0 and gameMap[i - 1][j] != 0):
        #                 if valueMap[i][j].getWeight(type) != 0:
        #                     result.append(str(i) + ":" + str(j))
        #                     size += 1
        #                 if size == 8:
        #                     return result
        #     return result
        #
        # def getHorizontalTargets(gameMap, valueMap):
        #     result = []
        #     size = 0
        #     for i in range(12):
        #         for j in range(7):
        #             if (i == 0 and gameMap[i][j] == 0 and gameMap[i][j + 1] == 0) or (
        #                     gameMap[i][j] == 0 and gameMap[i][j + 1] == 0 and gameMap[i - 1][j] != 0 and
        #                     gameMap[i - 1][j + 1] != 0):
        #                 if (i == 4 and j == 1):
        #                     print("gotcha")
        #                     print(numpy.flipud(gameMap))
        #                 if valueMap[i][j].getWeight(party) != 0 or valueMap[i][j + 1] != 0:
        #                     result.append(str(i) + ":" + str(j))
        #                     size += 1
        #                 if size == 4:
        #                     return result
        #     return result
        #
        # self.vtargets = getVerticalTargets(self.gameMap, self.valueMap)
        # self.htargets = getHorizontalTargets(self.gameMap, self.valueMap)

        # TODO: всё ещё надо над этим поработать
        def getRecycles(gameMap):
            result = []
            size = 0
            for i in range(12):
                for j in range(8):
                    if i == 0 and j < 8 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j] == 0 and \
                            gameMap[i + 1][j + 1] == 0:
                        result.append(str(i) + ":" + str(j) + ";" + str(i) + ":" + str(j + 1))
                        size += 2
                    if 0 < i < 12 and gameMap[i][j] != 0 and gameMap[i + 1][j] == 0:
                        result.append((i - 1) + ":" + j + ";" + i + ":" + j)
                        size += 1
                        if j < 8 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j + 1] == 0:
                            result.append(i + ":" + j + ";" + i + ":" + (j + 1))
                            size += 1
                    if i == 12 and gameMap[i][j] != 0:
                        result.append((i - 1) + ":" + j + ";" + i + ":" + j)
                        size += 1
                        if j < 8 and gameMap[i][j + 1] != 0:
                            result.append(i + ":" + j + ";" + i + ":" + (j + 1))
                            size += 1
                    if size >= 16:
                        return result
            return result

        self.recycles = []
        if moveNum > 24:
            self.recycles = getRecycles(self.gameMap)

        # here we place move heuristic weight (as discussed OUR MAX- ENEMY MAX)
        # which represents h()
        def getOwnWeight(valueMap):
            if party == 0:  # maybe 1 stays for dots?
                return Appraiser().getScoreColors(valueMap, self.gameMap)
            else:
                return Appraiser().getScoreDots(valueMap, self.gameMap)

        self.weight = getOwnWeight(self.valueMap)

        # here we detect if it's a goal state
        # would reuse victoryCheck, but need to refactor it a bit
        self.goalState = self.validator.victoryCheck(party, gameMap)

        def childcreator(moveString):
            move = Move(moveString)
            # print(moveString)
            if self.validator.placeValidator(move, gameMap):
                newGameMap = copy.copy(self.gameMap)
                newValueMap = copy.deepcopy(self.valueMap)
                newValidator = copy.copy(self.validator)

                Placer().place(move, newValidator, newGameMap)
                Appraiser().appraise(move, newValueMap, newGameMap)

                childNode = Treenode(depth - 1, newValueMap, newGameMap, moveNum + 1, newValidator, self.party)
                childNode.rawMove = moveString
                self.children.append(childNode)

        def populateChildren(candidates):
            for candidate in candidates:
                childcreator(candidate.move)

        if self.depth > 0 and self.goalState == 'go':
            populateChildren(self.candidates)

    def getMove(self):
        nextMove = self.children[0]
        for node in self.children:
            if nextMove.weight < node.weight:
                nextMove = node
        return nextMove.rawMove
