from validator import Validator
from move import Move
from placer import Placer
import copy

numbToLetter = {
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
            7: "G",
            8: "H"
        }


class Treenode:
    def __init__(self, depth, valueMap, gameMap, moveNum, validator, party):
        self.depth = depth
        self.gameMap = gameMap
        self.valueMap = valueMap
        self.children = []
        self.moveNum = moveNum
        self.validator = validator
        self.party = party



        def getTargets(gameMap, valueMap):
            result = []
            size = 0
            for i in range(12):
                for j in range(8):
                    if (gameMap[i][j] == 0 and gameMap[i - 1][j] != 0) or (i == 0 and gameMap[i][j] == 0):
                        if valueMap[i][j].totalWeight != 0:
                            result.append(i + ":" + j)
                            size += 1
                        if size == 8:
                            return result
            return result

        self.targets = getTargets(self.gameMap, self.valueMap)

        def getRecycles(gameMap):
            result = []
            size = 0
            for i in range(12):
                for j in range(8):
                    if i == 0 and j < 8 and gameMap[i][j] != 0 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j] == 0 and \
                            gameMap[i + 1][j + 1] == 0:
                        result.append(i + ":" + j + ";" + i + ":" + (j + 1))
                        size += 2
                    if 0 < i < 12 and gameMap[i][j] != 0 and gameMap[i + 1][j] == 0:
                        result.append((i-1) + ":" + j + ";" + i + ":" + j)
                        size += 1
                        if j < 8 and gameMap[i][j + 1] != 0 and gameMap[i + 1][j + 1] == 0:
                            result.append(i + ":" + j + ";" + i + ":" + (j + 1))
                            size += 1
                    if i == 12 and gameMap[i][j] != 0:
                        result.append((i-1) + ":" + j + ";" + i + ":" + j)
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
            # black magic
            return 0

        pass

        self.weight = getOwnWeight(self.valueMap)

        # here we detect if it's a goal state
        # would reuse victoryCheck, but need to refactor it a bit
        self.goalState = self.validator.victoryCheck(party)

        def populateChildren(targets, recycles):
            for coordinate in targets:
                i = coordinate.split(":")[0]
                j = coordinate.split(":")[1]
                for position in range(8):
                    move = Move('0 ' + position + ' ' + numbToLetter.get(j) + ' ' + i)
                    if self.validator.placeValidator(move):
                        newGameMap = copy.copy(self.gameMap)
                        newValueMap = copy.copy(self.valueMap)
                        newValidator = copy.copy(self.validator)
                        Placer.place(move, newGameMap)
                        # here we place nasty valueMap updater method call, which updates newValueMap based on the
                        # newGameMap
                        childNode = Treenode(depth - 1, newValueMap, newGameMap, self.party, validator)
                        self.children.append(childNode)
                    if self.moveNum > 24:
                        for recycle in self.recycles:
                            i1 = recycle.split(";")[0].split(":")[0]
                            j1 = recycle.split(";")[0].split(":")[1]
                            i2 = recycle.split(";")[1].split(":")[0]
                            j2 = recycle.split(";")[1].split(":")[1]
                            recycleMove = Move(numbToLetter.get(j1) + ' ' + i1 + ' ' + numbToLetter.get(j2) + ' ' + i2
                                               + ' ' + position + ' ' + +numbToLetter.get(j) + ' ' + i)
                            if self.validator.recycleValidator(recycleMove):
                                newGameMap = copy.copy(self.gameMap)
                                newValueMap = copy.copy(self.valueMap)
                                newValidator = copy.copy(self.validator)
                                Placer.place(move, newValidator, gameMap)
                                # here we place nasty valueMap updater method call, which updates newValueMap based
                                # on the newGameMap
                                childNode = Treenode(depth - 1, newValueMap, newGameMap)
                                self.children.append(childNode)

        if self.depth > 0 and self.goalState == 0:
            populateChildren(self.targets)
