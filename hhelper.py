# heuristic helper to operates with
from move import Move

class Hhelper:
    def __init__(self, valueMap):
        self.valueMap = valueMap


    def verticalRowCheck(self, address):
        pass

    def horizontalRowCheck(self, address):
        pass

    def diagonalRowCheck(self,address):
        pass

    def update(self, move):
        pass

    def borderCheck(self, i, j):
        if ( 0<=i<8 and 0<=j<12):
            return True
        else:
            return False


