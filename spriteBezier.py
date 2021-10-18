import pygame

#Colors
blue1 = (40, 70, 200)
blue2 = (0, 150, 255)
red = (255, 0, 0)
green = (0, 255, 150)
yellow = (150, 150, 50)
yellow2 = (250,250,10)
purple = (250, 0, 250)

pygame.init()

FPS = 70
fpsClock = pygame.time.Clock()
sprite = pygame.image.load("assets/mochi.png")
# sprite.get_rect()

goingUp = True
exist = False

lerp = 50
points = []
lines = []
lerpPoints = []

lerpPoints2 = []
lerpLines = []

lerpPoints3 = []
lerpLines2 = []

curvePoints = []


screen = pygame.display.set_mode([800,600])

def render():
    screen.fill((255,255,255))
    # for line in lines:
    #     pygame.draw.line(screen, blue1, line[0], line[1], 3)

    # for point in points:
    #     pygame.draw.circle(screen, red, point, 5)
    
    # for point in lerpPoints:
    #     pygame.draw.circle(screen, blue2, point, 5)

    # for lerpLine in lerpLines:
    #     pygame.draw.line(screen, yellow, lerpLine[0], lerpLine[1], 3)
    
    # for point in lerpPoints2:
    #     pygame.draw.circle(screen, yellow2, point, 5)

    # for point in curvePoints:
    #     pygame.draw.circle(screen, purple, point, 2)


    # for line in lerpLines2:
    #     pygame.draw.line(screen, red, line[0], line[1], 3)

    for point in lerpPoints3:
        # pygame.draw.circle(screen, blue1, point, 5)
        screen.blit(sprite, point)
        



running = True
while running:
    render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            points.append((x,y))
            if len(points) >=2:
                lines.append([points[-2], points[-1]])
            if len(lines) >= 1:
                lerpPoints.append(points[len(points)-1])
            if len(lerpPoints) >= 2:
                lerpLines.append([lerpPoints[-2], lerpPoints[-1]])
            if len(lerpLines) >= 1:
                lerpPoints2.append(lerpPoints[len(lerpPoints)-1])
            if len(lerpLines2) >= 1:
                lerpPoints3.append(lerpPoints2[-1])
            if len(curvePoints) >= 1:
                curvePoints = []

            if len(points) >= 4:
                lerpLines2.append([lerpPoints2[-2], lerpPoints2[-1]])
                lerpPoints3.append(lerpLines[-1][0])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                points = []
                lines = []
                lerpPoints = []
                lerpPoints2 = []
                lerpLines = []
                lerpPoints3 = []
                lerpLines2 = []
                curvePoints = []

    if lerp >= 100:
        goingUp = False
    if lerp <= 0:
        goingUp = True

    if goingUp:
        lerp += 1
    if not goingUp:
        lerp -= 1
    for i in range(len(lerpPoints)):
        if len(lerpPoints) >= 0:
            increment = (lines[i][1][1] - lines[i][0][1], lines[i][1][0] - lines[i][0][0])
            newPoint = (lines[i][0][0] + increment[1] * (lerp/100), lines[i][0][1] + increment[0] * (lerp/100))
            lerpPoints[i] = newPoint
    
    if len(lerpLines) >= 1:
        for i in range(len(lerpLines)):
            lerpLines[i][0] = lerpPoints[i]
            lerpLines[i][1] = lerpPoints[i + 1]
    
    if len(lerpPoints2) >= 1:
        for i in range(len(lerpPoints2)):
            increment = (lerpLines[i][1][1] - lerpLines[i][0][1], lerpLines[i][1][0] - lerpLines[i][0][0])
            newPoint = (lerpLines[i][0][0] + increment[1] * (lerp/100), lerpLines[i][0][1] + increment[0] * lerp/100)
            lerpPoints2[i] = newPoint

    for i in range(len(lerpLines2)):
        lerpLines2[i][0] = lerpPoints2[i]
        lerpLines2[i][1] = lerpPoints2[i + 1]

    if len(lerpLines2) >= 1:
        for i in range(len(lerpPoints3)):
            increment = (lerpLines2[i][1][1] - lerpLines2[i][0][1], lerpLines2[i][1][0] - lerpLines2[i][0][0])
            newPoint = (lerpLines2[i][0][0] + increment[1] * lerp/100, lerpLines2[i][0][1] + increment[0] * lerp/100)
            lerpPoints3[i] = newPoint
    


    if len(lerpPoints2) >= 1:
        if len(points) < 4:
            yeee = lerpPoints2[-1]
        if len(points) >= 4:
            yeee = lerpPoints3[-1]
        for i in curvePoints:
            if i == yeee:
                exist = True
            # pygame.draw.circle(screen, green, i, 2)
        if exist == False:
            curvePoints.append(yeee)
            exist = True
        exist = False


    fpsClock.tick(FPS)
    pygame.display.flip()