class Level(object):

    def __init__(self, style, plays = 0, clears = 0):
        self.style = style
        self.current = "over"
        self.overBoard = [[0] * 240 for row in range(27)]
        self.waterBoard = [[0] * 240 for row in range(27)]
        self.underBoard = [[0] * 240 for row in range(27)]

        self.plays = 0
        self.clears = 0