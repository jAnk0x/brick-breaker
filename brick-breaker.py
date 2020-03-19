import pygame
import sys
import random
import math

pygame.init()

class ball:
    def __init__(self):
        self.x = 250
        self.y = 250
        self.radius = 10
        self.vector = self.convertToUnit([1, 4])
        self.vector[0] = int(self.vector[0] * 5)
        self.vector[1] = int(self.vector[1] * 5)
        self.score = 0

    def move(self, bouncer, bricks):
        changeX = self.vector[0]
        changeY = self.vector[1]

        if self.x + changeX - self.radius < 0: # left wall collision
            self.x = self.radius
            changeX = 0
            self.vector[0] *= -1
        elif self.x + changeX + self.radius > windowWidth: # right wall colision
            self.x = windowWidth - self.radius
            changeX = 0
            self.vector[0] *= -1
        elif self.y + changeY + self.radius >= 485 and \
            (self.x + changeX + self.radius >= bouncer.left and self.x + changeX - self.radius <= bouncer.right): # bouncer collision
            self.y = 485 - self.radius
            changeY = 0
            self.vector[1] *= -1
        elif self.y + changeY - self.radius < 0: # upper wall collision
            self.y = self.radius
            changeY = 0
            self.vector[1] *= -1
        elif self.y - self.radius > 500:
            gameOver(self.score, False)
        else: # brick collision
            for brickComplex in bricks:
                brick = brickComplex[0]
                if self.y + changeY - self.radius <= brick.bottom and self.y + changeY + self.radius >= brick.top and \
                    (self.x + changeX + self.radius >= brick.left and self.x + changeX - self.radius <= brick.right):
                    if self.y - self.radius > brick.bottom: # bottom collision
                        self.y = brick.bottom + self.radius
                        changeY = 0
                        self.vector[1] *= -1
                    elif self.y + self.radius < brick.top: # top collision
                        self.y = brick.top - self.radius
                        changeY = 0
                        self.vector[1] *= -1
                    elif self.x + self.radius < brick.left: # left side collision
                        self.x = brick.left - self.radius
                        changeX = 0
                        self.vector[0] *= -1
                    else: # right side collision
                        self.x = brick.right + self.radius
                        changeX = 0
                        self.vector[0] *= -1
                    
                    bricks.remove(brickComplex)
                    self.score += 1
                    pygame.display.set_caption("Score: " + str(self.score))
                    
                    if len(bricks) == 0:
                        gameOver(self.score, True)
                    break

        self.x += changeX
        self.y += changeY

    def convertToUnit(self, vector):
        mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        return [vector[0] / mag, vector[1] / mag]

windowWidth = 500
windowHeight = windowWidth
window = pygame.display.set_mode((windowWidth, windowHeight))
fps = pygame.time.Clock()

def moveBouncer(dir,  bouncer):
    if dir == "left":
        if bouncer.left - 4 < 0:
            bouncer.left = 0
        else:
            bouncer.left -= 4
    if dir == "right":
        if bouncer.right + 4 > windowWidth:
            bouncer.right = windowWidth
        else:
            bouncer.right += 4

def createBricks(brickW, brickH):
    bricks = []
    for x in range(1, windowWidth, 50):
        for y in range(0, brickH * 3 + 3, brickH + 1):
            bricks.append([pygame.Rect(x, y, brickW, brickH), (random.randrange(0, 226), random.randrange(0, 226), random.randrange(0, 226))])
    return bricks

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True

def gameOver(score, isVictory):
    font = pygame.font.SysFont('arial', 32) 

    if isVictory:
        victoryText = font.render("You win!", True, (0, 160, 0)) 
        victoryTextRect = victoryText.get_rect()
        victoryTextRect.center = (windowWidth // 2, windowHeight // 2 - 50) 
        window.blit(victoryText, victoryTextRect)
    else:
        lossText = font.render(":(", True, (255, 0, 0)) 
        lossTextRect = lossText.get_rect()
        lossTextRect.center = (windowWidth // 2, windowHeight // 2 - 50) 
        window.blit(lossText, lossTextRect)
            
    message = "Score: " + str(score)
    text = font.render(message, True, (0, 0, 255)) 
    textRect = text.get_rect()  
    textRect.center = (windowWidth // 2, windowHeight // 2) 
    window.blit(text, textRect)
    pygame.display.update()
    if wait():
        main(ball()) 

def quit():
    pygame.quit()
    sys.exit()

def main(ball):
    pygame.display.set_caption("Game")

    bricks = createBricks(48, 20)
    bouncer = pygame.Rect(220, 485, 60, 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            moveBouncer("left", bouncer)
        if keys[pygame.K_RIGHT]:
            moveBouncer("right", bouncer)

        window.fill(pygame.Color(225, 225, 225))

        for brick in bricks:
            color = brick[1]
            pygame.draw.rect(window, pygame.Color(color[0], color[1], color[2]), brick[0])
        pygame.draw.rect(window, pygame.Color(225, 0, 0), bouncer)

        pygame.draw.circle(window, (0, 0, 225), (ball.x, ball.y), ball.radius)
        ball.move(bouncer, bricks)

        pygame.display.flip()
        fps.tick(60)

if __name__ == "__main__":
    main(ball())