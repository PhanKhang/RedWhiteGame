import re


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

        self.rawMove = input

        def validateFormat(input):
            pattern = re.compile(
                "(^[A-H]\s([1-9]|[1][0-2])\s[A-H]\s([1-9]|[1][0-2])\s[1-8]\s[A-H]\s([1-9]|[1][0-2])|"
                "^[0]\s[1-8]\s[A-H]\s([1-9]|[1][0-2]))$")
            if not pattern.match(input):
                raise Exception("Invalid input")

        validateFormat(input)

        self.input = input.split(" ")

        def parseType(input):
            if input[:1].isdigit():
                return 0
            return 1

        self.type = parseType(input)

        def parseRotation(input, type):
            if type == 0:
                return int(input[1])
            return int(input[4])

        def parseTargetCoordinateNum(input, type):
            if type == 0:
                return int(input[3])
            return int(input[6])

        def parseTargetCoordinateLet(input, type):
            if type == 0:
                return int(letterTonumb.get(input[2]))
            return int(letterTonumb.get(input[5]))

        def parseSourceCoordinate1Num(input, type):
            if type == 1:
                return int(input[1])
            return None

        def parseSourceCoordinate1Let(input, type):
            if type == 1:
                return int(letterTonumb.get(input[0]))
            return None

        def parseSourceCoordinate2Num(input, type):
            if type == 1:
                return int(input[3])
            return None

        def parseSourceCoordinate2Let(input, type):
            if type == 1:
                return int(letterTonumb.get(input[2]))
            return None

        self.rotation = parseRotation(self.input, self.type)
        self.targetCoordinateNum = parseTargetCoordinateNum(self.input, self.type)
        self.targetCoordinateLet = parseTargetCoordinateLet(self.input, self.type)
        self.sourceCoordinate1Num = parseSourceCoordinate1Num(self.input, self.type)
        self.sourceCoordinate1Let = parseSourceCoordinate1Let(self.input, self.type)
        self.sourceCoordinate2Num = parseSourceCoordinate2Num(self.input, self.type)
        self.sourceCoordinate2Let = parseSourceCoordinate2Let(self.input, self.type)
