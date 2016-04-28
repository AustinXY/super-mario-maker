class Level(object):

    def __init__(self, style, plays = 0, clears = 0):
        self.style = style
        self.current = "over"
        self.overBoard = [[0] * 240 for row in range(27)]
        self.waterBoard = [[0] * 240 for row in range(27)]
        self.underBoard = [[0] * 240 for row in range(27)]

        self.plays = 0
        self.clears = 0

        self.startPlaced = False
        self.endPlaced = False

    def getCurrent(self):
        return self.current

    def getMap(self):
        if(self.current == "over"):
            return self.overBoard
        elif(self.current == "water"):
            return self.waterBoard
        elif(self.current == "under"):
            return self.underBoard

    def setEntity(self, board, entity, row, col):
        if(entity == 0):
            self.removeEntity(board, row, col)
        elif((entity == "start" and self.startPlaced) or (entity == "end" and self.endPlaced)):
            pass
        elif(board == "over"):
            if(entity == "start"):
                self.startPlaced = True
            if(entity == "end"):
                self.endPlaced = True

            if(self.overBoard[row][col] == 0):
                self.overBoard[row][col] = entity
            elif(self.overBoard[row][col] == "question" and entity == "mushroom"):
                self.overBoard[row][col] = "question1"
            elif(self.overBoard[row][col] == "question" and entity == "flower"):
                self.overBoard[row][col] = "question2"
        elif(board == "water"):
            if(self.waterBoard[row][col] == 0):
                self.waterBoard[row][col] = entity
        elif(board == "under"):
            if(self.underBoard[row][col] == 0):
                self.underBoard[row][col] = entity

    def removeEntity(self, board, row, col):
        if(board == "over"):
            if(self.overBoard[row][col] == "start"):
                self.startPlaced = False
            elif(self.overBoard[row][col] == "end"):
                self.endPlaced = False
            self.overBoard[row][col] = 0
        elif(board == "water"):
            self.waterBoard[row][col] = 0
        elif(board == "under"):
            self.underBoard[row][col] = 0

    def getStart(self):
        for row in range(len(self.overBoard)):
            if("start" in self.getMap()[row]):
                return (row, self.getMap()[row].index("start"))
        return None

    def loadFromSave(self, saveData):
        self.overBoard = saveData[0]
        self.underBoard = saveData[1]
        self.waterBoard = saveData[2]
        self.style = saveData[3]
        self.plays = saveData[4]
        self.clears = saveData[5]