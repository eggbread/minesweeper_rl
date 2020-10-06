import random, pygame, sys, time
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 600
BOXSIZE = 30
GAPSIZE = 5
FIELDWIDTH = 10
FIELDHEIGHT = 10
XMARGIN = int((WINDOWWIDTH - (FIELDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = XMARGIN
MINESTOTAL = 10

def reset_position(self):
    self.box_x = None
    self.box_y = None
    self.mouseClicked = False


def click(self, x, y):
    self.box_x = x
    self.box_y = y
    self.mouseClicked = True
    return x, y


def reset_game(self):
    self.reset_flag = True


def blankField(self):
    # creates blank FIELDWIDTH x FIELDHEIGHT data structure

    field = []
    for x in range(FIELDWIDTH):
        field.append([])
        for y in range(FIELDHEIGHT):
            field[x].append('[ ]')
    return field


def placeMines(self, field):
    # places mines in FIELDWIDTH x FIELDHEIGHT data structure
    # requires blank field as input

    mineCount = 0
    xy = []
    while mineCount < MINESTOTAL:
        x = random.randint(0, FIELDWIDTH - 1)
        y = random.randint(0, FIELDHEIGHT - 1)
        xy.append([x, y])
        if xy.count([x, y]) > 1:
            xy.remove([x, y])
        else:
            field[x][y] = '[X]'
            mineCount += 1


def isThereMine(self, field, x, y):
    # checks if mine is located at specific box on field

    return field[x][y] == '[X]'


def placeNumbers(self, field):
    # places numbers in FIELDWIDTH x FIELDHEIGHT data structure
    # requires field with mines as input

    for x in range(FIELDWIDTH):
        for y in range(FIELDHEIGHT):
            if not self.isThereMine(field, x, y):
                count = 0
                if x != 0:
                    if self.isThereMine(field, x - 1, y):
                        count += 1
                    if y != 0:
                        if self.isThereMine(field, x - 1, y - 1):
                            count += 1
                    if y != FIELDHEIGHT - 1:
                        if self.isThereMine(field, x - 1, y + 1):
                            count += 1
                if x != FIELDWIDTH - 1:
                    if self.isThereMine(field, x + 1, y):
                        count += 1
                    if y != 0:
                        if self.isThereMine(field, x + 1, y - 1):
                            count += 1
                    if y != FIELDHEIGHT - 1:
                        if self.isThereMine(field, x + 1, y + 1):
                            count += 1
                if y != 0:
                    if self.isThereMine(field, x, y - 1):
                        count += 1
                if y != FIELDHEIGHT - 1:
                    if self.isThereMine(field, x, y + 1):
                        count += 1
                field[x][y] = '[%s]' % (count)


def blankRevealedBoxData(self, val):
    # returns FIELDWIDTH x FIELDHEIGHT data structure different from the field data structure
    # each item in data structure is boolean (val) to show whether box at those fieldwidth & fieldheight coordinates should be revealed

    revealedBoxes = []
    for i in range(FIELDWIDTH):
        revealedBoxes.append([val] * FIELDHEIGHT)
    return revealedBoxes


def gameSetup(self):
    # set up mine field data structure, list of all zeros for recursion, and revealed box boolean data structure

    mineField = self.blankField()
    self.placeMines(mineField)
    self.placeNumbers(mineField)
    zeroListXY = []
    markedMines = []
    revealedBoxes = self.blankRevealedBoxData(False)

    return mineField, zeroListXY, revealedBoxes, markedMines


def drawField(self):
    # draws field GUI and reset button

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            left, top = self.getLeftTopXY(box_x, box_y)
            pygame.draw.rect(DISPLAYSURFACE, BOXCOLOR_REV, (left, top, BOXSIZE, BOXSIZE))

    DISPLAYSURFACE.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURFACE.blit(SHOW_SURF, SHOW_RECT)


def drawMinesNumbers(self, field):
    # draws mines and numbers onto GUI
    # field should have mines and numbers

    half = int(BOXSIZE * 0.5)
    quarter = int(BOXSIZE * 0.25)
    eighth = int(BOXSIZE * 0.125)

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            left, top = self.getLeftTopXY(box_x, box_y)
            center_x, center_y = self.getCenterXY(box_x, box_y)
            if field[box_x][box_y] == '[X]':
                pygame.draw.circle(DISPLAYSURFACE, MINECOLOR, (left + half, top + half), quarter)
                pygame.draw.circle(DISPLAYSURFACE, WHITE, (left + half, top + half), eighth)
                pygame.draw.line(DISPLAYSURFACE, MINECOLOR, (left + eighth, top + half),
                                 (left + half + quarter + eighth, top + half))
                pygame.draw.line(DISPLAYSURFACE, MINECOLOR, (left + half, top + eighth),
                                 (left + half, top + half + quarter + eighth))
                pygame.draw.line(DISPLAYSURFACE, MINECOLOR, (left + quarter, top + quarter),
                                 (left + half + quarter, top + half + quarter))
                pygame.draw.line(DISPLAYSURFACE, MINECOLOR, (left + quarter, top + half + quarter),
                                 (left + half + quarter, top + quarter))
            else:
                for i in range(1, 9):
                    if field[box_x][box_y] == '[' + str(i) + ']':
                        if i in range(1, 3):
                            textColor = TEXTCOLOR_1
                        else:
                            textColor = TEXTCOLOR_2
                        self.drawText(str(i), BASICFONT, textColor, DISPLAYSURFACE, center_x, center_y)


def showNumbers(self, revealedBoxes, mineField, box_x, box_y, zeroListXY):
    # modifies revealedBox data strucure if chosen box_x & box_y is [0]
    # show all boxes using recursion

    revealedBoxes[box_x][box_y] = True
    self.revealAdjacentBoxes(revealedBoxes, box_x, box_y)
    for i, j in self.getAdjacentBoxesXY(mineField, box_x, box_y):
        if mineField[i][j] == '[0]' and [i, j] not in zeroListXY:
            zeroListXY.append([i, j])
            self.showNumbers(revealedBoxes, mineField, i, j, zeroListXY)


def showMines(self, revealedBoxes, mineField, box_x, box_y):
    # modifies revealedBox data strucure if chosen box_x & box_y is [X]

    for i in range(FIELDWIDTH):
        for j in range(FIELDHEIGHT):
            if mineField[i][j] == '[X]':
                revealedBoxes[i][j] = True


def revealAdjacentBoxes(self, revealedBoxes, box_x, box_y):
    # modifies revealedBoxes data structure so that all adjacent boxes to (box_x, box_y) are set to True

    if box_x != 0:
        revealedBoxes[box_x - 1][box_y] = True
        if box_y != 0:
            revealedBoxes[box_x - 1][box_y - 1] = True
        if box_y != FIELDHEIGHT - 1:
            revealedBoxes[box_x - 1][box_y + 1] = True
    if box_x != FIELDWIDTH - 1:
        revealedBoxes[box_x + 1][box_y] = True
        if box_y != 0:
            revealedBoxes[box_x + 1][box_y - 1] = True
        if box_y != FIELDHEIGHT - 1:
            revealedBoxes[box_x + 1][box_y + 1] = True
    if box_y != 0:
        revealedBoxes[box_x][box_y - 1] = True
    if box_y != FIELDHEIGHT - 1:
        revealedBoxes[box_x][box_y + 1] = True


def getAdjacentBoxesXY(self, mineField, box_x, box_y):
    # get box XY coordinates for all adjacent boxes to (box_x, box_y)

    adjacentBoxesXY = []

    if box_x != 0:
        adjacentBoxesXY.append([box_x - 1, box_y])
        if box_y != 0:
            adjacentBoxesXY.append([box_x - 1, box_y - 1])
        if box_y != FIELDHEIGHT - 1:
            adjacentBoxesXY.append([box_x - 1, box_y + 1])
    if box_x != FIELDWIDTH - 1:
        adjacentBoxesXY.append([box_x + 1, box_y])
        if box_y != 0:
            adjacentBoxesXY.append([box_x + 1, box_y - 1])
        if box_y != FIELDHEIGHT - 1:
            adjacentBoxesXY.append([box_x + 1, box_y + 1])
    if box_y != 0:
        adjacentBoxesXY.append([box_x, box_y - 1])
    if box_y != FIELDHEIGHT - 1:
        adjacentBoxesXY.append([box_x, box_y + 1])

    return adjacentBoxesXY


def drawCovers(self, revealedBoxes, markedMines):
    # uses revealedBox FIELDWIDTH x FIELDHEIGHT data structure to determine whether to draw box covering mine/number
    # draw red cover instead of gray cover over marked mines

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            if not revealedBoxes[box_x][box_y]:
                left, top = self.getLeftTopXY(box_x, box_y)
                if [box_x, box_y] in markedMines:
                    pygame.draw.rect(DISPLAYSURFACE, MINEMARK_COV, (left, top, BOXSIZE, BOXSIZE))
                else:
                    pygame.draw.rect(DISPLAYSURFACE, BOXCOLOR_COV, (left, top, BOXSIZE, BOXSIZE))


def drawText(self, text, font, color, surface, x, y):
    # function to easily draw text and also return object & rect pair

    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)


def drawButton(self, text, color, bgcolor, center_x, center_y):
    # similar to drawText but text has bg color and returns obj & rect

    butSurf = BASICFONT.render(text, True, color, bgcolor)
    butRect = butSurf.get_rect()
    butRect.centerx = center_x
    butRect.centery = center_y

    return (butSurf, butRect)


def getLeftTopXY(self, box_x, box_y):
    # get left & top coordinates for drawing mine boxes

    left = XMARGIN + box_x * (BOXSIZE + GAPSIZE)
    top = YMARGIN + box_y * (BOXSIZE + GAPSIZE)
    return left, top


def getCenterXY(self, box_x, box_y):
    # get center coordinates for drawing mine boxes

    center_x = XMARGIN + BOXSIZE / 2 + box_x * (BOXSIZE + GAPSIZE)
    center_y = YMARGIN + BOXSIZE / 2 + box_y * (BOXSIZE + GAPSIZE)
    return center_x, center_y


def getBoxAtPixel(self, x, y):
    # gets coordinates of box at mouse coordinates

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            left, top = self.getLeftTopXY(box_x, box_y)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (box_x, box_y)
    return (None, None)


def highlightBox(self, box_x, box_y):
    # highlight box when mouse hovers over it

    left, top = self.getLeftTopXY(box_x, box_y)
    pygame.draw.rect(DISPLAYSURFACE, HILITECOLOR, (left, top, BOXSIZE, BOXSIZE), 4)


def highlightButton(self, butRect):
    # highlight button when mouse hovers over it

    linewidth = 4
    pygame.draw.rect(DISPLAYSURFACE, HILITECOLOR, (
        butRect.left - linewidth, butRect.top - linewidth, butRect.width + 2 * linewidth,
        butRect.height + 2 * linewidth), linewidth)


def gameWon(self, revealedBoxes, mineField):
    # check if player has revealed all boxes

    notMineCount = 0

    for box_x in range(FIELDWIDTH):
        for box_y in range(FIELDHEIGHT):
            if revealedBoxes[box_x][box_y] == True:
                if mineField[box_x][box_y] != '[X]':
                    notMineCount += 1

    if notMineCount >= (FIELDWIDTH * FIELDHEIGHT) - MINESTOTAL:
        return True
    else:
        return False


def gameOverAnimation(self, mineField, revealedBoxes, markedMines, result):
    # makes background flash red (loss) or blue (win)

    origSurf = DISPLAYSURFACE.copy()
    flashSurf = pygame.Surface(DISPLAYSURFACE.get_size())
    flashSurf = flashSurf.convert_alpha()
    animationSpeed = 20

    if result == 'WIN':
        r, g, b = BLUE
    else:
        r, g, b = RED

    for i in range(5):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):  # animation loop
                self.checkForKeyPress()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURFACE.blit(origSurf, (0, 0))
                DISPLAYSURFACE.blit(flashSurf, (0, 0))
                pygame.draw.rect(DISPLAYSURFACE, FIELDCOLOR, (
                    XMARGIN - 5, YMARGIN - 5, (BOXSIZE + GAPSIZE) * FIELDWIDTH + 5,
                    (BOXSIZE + GAPSIZE) * FIELDHEIGHT + 5))
                self.drawField()
                self.drawMinesNumbers(mineField)
                tipFont = pygame.font.SysFont(FONTTYPE, 16)  ## not using BASICFONT - too big
                self.drawText('Tip: Highlight a box and press space (rather than click the mouse)', tipFont,
                              TEXTCOLOR_3, DISPLAYSURFACE, WINDOWWIDTH / 2, WINDOWHEIGHT - 60)
                self.drawText('to mark areas that you think contain mines.', tipFont, TEXTCOLOR_3, DISPLAYSURFACE,
                              WINDOWWIDTH / 2, WINDOWHEIGHT - 40)
                RESET_SURF, RESET_RECT = self.drawButton('RESET', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH / 2,
                                                         WINDOWHEIGHT - 120)
                SHOW_SURF, SHOW_RECT = self.drawButton('SHOW ALL', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH / 2,
                                                       WINDOWHEIGHT - 95)
                self.drawCovers(revealedBoxes, markedMines)
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def terminate(self):
    # simple function to exit game

    pygame.quit()
    sys.exit()


def checkForKeyPress(self):
    # check if quit or any other key is pressed

    if len(pygame.event.get(QUIT)) > 0:
        self.terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        self.terminate()
    return keyUpEvents[0].key