class Button(object):

    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y

def getCellCorner(data, row, col):
    return (data.MARGIN + data.GRID_SIZE * row, 
        data.MARGIN + data.GRID_SIZE * col)

def getCell(data, x, y):
    if(x < data.MARGIN or x > data.width or 
        y < data.MARGIN or y > data.height):
        return None
    else:
        return ((x - data.MARGIN) // data.GRID_SIZE + data.xOffset, 
            (y - data.MARGIN) // data.GRID_SIZE + data.yOffset)

def getOnscreenCell(data, x, y):
    if(x < data.MARGIN or x > data.width or 
        y < data.MARGIN or y > data.height):
        return None
    else:
        return ((x - data.MARGIN) // data.GRID_SIZE, 
            (y - data.MARGIN) // data.GRID_SIZE)
