# Heuristic helper, value storage cell.
class Cell:
    occupied: int = 0
    redWeight: int = 0
    whiteWeight: int = 0
    ringWeight: int = 0
    dotWeight: int = 0
    target: int = 0
    totalWeight: int = 0


    def update(self):
        self.totalWeight = (self.dotWeight + self.redWeight + self.ringWeight + self.whiteWeight)/4
