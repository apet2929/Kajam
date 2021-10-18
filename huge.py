import pygame
import random
import pygame.draw

pygame.init()


#Init Vars
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.RESIZABLE)
FPS = 10
fpsClock = pygame.time.Clock()
global state
state = 0
subState = 0

txtCol = 1
col1 = 1

def menuState():
    global start
    screen.fill((180, 50, 50))
    Text("Save Hooman", WIDTH/15, (255,255,255), (255,255,255), True, 0, HEIGHT/4)
    start = Button(pygame.Rect(WIDTH/2 - WIDTH/8, HEIGHT/2, WIDTH/4, HEIGHT/6), "Start", WIDTH/20, (255,0,0), (100,0,90), (255,255,255), 40)

def menuStateInput(event):
    global state
    if event.type == pygame.MOUSEBUTTONDOWN:
        if start.checkClick():
            print("clicked=True")
            state = 1

def tutorialState():
    screen.fill((255, 50, 0))

def tutorialStateInput(event):
    pass

#Main Functions~~~~~~~

def render():
    if state == 0:
        menuState()
    if state == 1:
        tutorialState()

def handleInput(event):
    if state == 0:
        menuStateInput(event)
    if state == 1:
        tutorialStateInput(event)



#Mechanics Functions~~~~~~~

class Text():
    def __init__(self, t, s=int(WIDTH/11), color=txtCol, underlineCol=col1, centerX=True, x=0, y=0, centerY=False):
        font = pygame.font.Font('font.ttf', int(s), bold=False, italic=False)
        self.text = font.render(t, True, color)
        self.x = x
        self.y = y
        
        self.underlineCol = underlineCol
        if centerX:
            self.x = WIDTH/2 - self.text.get_width()/2
        else:
            self.x -= self.text.get_width()/2
        if centerY:
            self.y -= self.text.get_height()/2
            pass

        print("yee")
        print(self.y)
        print(y)

        screen.blit(self.text, (self.x, self.y))

    
    def underline(self, dist = HEIGHT/50, wid = HEIGHT/70):
        pygame.draw.line(screen, self.underlineCol, (self.x + dist, self.y + self.text.get_height() + dist), (self.x + self.text.get_width() - dist, self.y + self.text.get_height() + dist), int(wid))

class Button():
    def __init__(self, rect, textLbl, textSize, col1, col2, txtCol, rad):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        c1 = [col1[0], col1[1], col1[2]]
        c2 = [col2[0], col2[1], col2[2]]
        c3 = []
        for i in range(int(self.height-rad)):
            c1[0] += (c2[0] - c1[0])/(self.height-rad)
            c1[1] += (c2[1] - c1[1])/(self.height-rad)
            c1[2] += (c2[2] - c1[2])/(self.height-rad)
            c3 = (c1[0], c1[1], c1[2])
            pygame.draw.rect(screen, c3, pygame.Rect(self.x, self.y + i, self.width, rad),  int(rad/2), rad)

        # print(self.x + self.width/2, self.y + self.height/2)
        Text(textLbl, int(textSize), txtCol, centerX=True,  y=self.y, centerY=False)
        # Text(textLbl, x=self.x, y=self.y)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x, self.y, self.width, self.height), 2)


    def checkClick(self):
        xPos, yPos = pygame.mouse.get_pos()
        if xPos in range(self.x, self.x + self.width) and yPos in range(self.y, self.y + self.height):
            return True
        else:
            return False


#Run da coed~~~~~~
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handleInput(event)
    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    render()
    
    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()