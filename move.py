class Move:
    # будет ли жто работать при координатах которые больше 9? у нас это возможно
    def __init__(self, input):

        letterTonumb = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8

        }

        def parseType(input):
            if input[:1].isdigit():
                return 0
            return 1

        self.type = parseType(input)

        def parseRotation(input, type):
            if type == 0:
                return input[1:2]
            return input[4:5]

        def parseTargetCoordinateNum(input, type):
            if type == 0:
                return input[3:4]
            return input[6:7]

        def parseTargetCoordinateLet(input, type):
            if type == 0:
                return letterTonumb.get(input[2:3])
            return letterTonumb.get(input[5:6])

        def parseSourceCoordinate1Num(input, type):
            if type == 1:
                return input[1:2]
            return None

        def parseSourceCoordinate1Let(input, type):
            if type == 1:
                return letterTonumb.get(input[:1])
            return None

        def parseSourceCoordinate2Num(input, type):
            if type == 1:
                return input[3:4]
            return None

        def parseSourceCoordinate2Let(input, type):
            if type == 1:
                return letterTonumb.get(input[2:3])
            return None

        self.rotation = parseRotation(input, self.type)
        self.targetCoordinateNum = parseTargetCoordinateNum(input, self.type)
        self.targetCoordinateLet = parseTargetCoordinateLet(input, self.type)
        self.sourceCoordinate1Num = parseSourceCoordinate1Num(input, self.type)
        self.sourceCoordinate1Let = parseSourceCoordinate1Let(input, self.type)
        self.sourceCoordinate2Num = parseSourceCoordinate2Num(input, self.type)
        self.sourceCoordinate2Let = parseSourceCoordinate2Let(input, self.type)
