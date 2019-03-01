# Heuristic helper, value storage cell.
class Cell:
    occupied: int = 0
    redWeight: int = 0
    whiteWeight: int = 0
    ringWeight: int = 0
    dotWeight: int = 0
    target: int = 0
    totalWeight: int = 0

    def getWeight(self, party):
        if party == '0':
            self.totalWeight = (self.dotWeight + self.ringWeight) - (self.whiteWeight + self.redWeight)
        elif party == '1':
            self.totalWeight = (self.redWeight + self.whiteWeight) - (self.dotWeight + self.ringWeight)
        return self.totalWeight
