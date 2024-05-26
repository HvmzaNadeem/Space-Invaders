#Name: Hamza Nadeem
#Project: Culminating Task ICS4U
#Due Date: 06/21/2022

#import libraries
import pygame, time
import random as r
import easygui as e

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#initilize pygame
pygame.init()

#screen setup
width, height = 800, 450
screen = pygame.display.set_mode ((width, height))
pygame.display.set_caption ("Invaders of Space")

#load images
playership = pygame.image.load("ship.png")
enemyship = pygame.image.load("enemy.png")
bg = pygame.image.load("background.png")
projectile = pygame.image.load("shipprojectile.png")
fH = pygame.image.load("fullheart.png")
bH = pygame.image.load("brokenheart.png")
Score = pygame.image.load("score.png")
extraHeart = pygame.image.load("hearts.png")

#display lives based on amount of lives remaining
def displayLives(lives):
	if (lives == 3):
		screen.blit(fH,(665,0))
		screen.blit(fH,(710,0))
		screen.blit(fH,(755,0))
	elif (lives == 2):
		screen.blit(fH,(665,0))
		screen.blit(fH,(710,0))
		screen.blit(bH,(755,0))
	elif (lives == 1):
		screen.blit(fH,(665,0))
		screen.blit(bH,(710,0))
		screen.blit(bH,(755,0))
	elif (lives == 0):
		screen.blit(bH,(665,0))
		screen.blit(bH,(710,0))
		screen.blit(bH,(755,0))

#player class
class Player(pygame.sprite.Sprite):
    #define paremeters for player ship
    def __init__ (self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
    
    #draw player ship
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

#class for enemy ship
class Enemy(pygame.sprite.Sprite):
    #define paremeters for enemy ship
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()

    #draw enemy ship
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    #move enemy ship down the screen based on velocity variable
    def move(self, vel):
        self.y += vel

#class for projectile
class Proj(pygame.sprite.Sprite):
    #define parameters for projectile
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()

    #draw projectile
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    #move the projectile based on velocity variable
    def move(self, vel):
        self.y -= vel

class gainLives(pygame.sprite.Sprite):
    #define parameters for heart
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def move(self, vel):
        self.y += vel



#initilize player
player = Player(375,325, playership)


#set game variables/lists
clock = pygame.time.Clock()
playerVel = 5
enemyVel = 2
enemyNumber = 0
enemyList = []
level = 0
lives = 3
projectiles = []
projVel = 4
projCooldown = False
timer = 0
score = 0
start = False
highscore = 0
hearts = []
heartVel = 3
heartTimer = 0

#set up text for variables
font = pygame.font.Font(None, 55)
stext = font.render(str(score), True, WHITE, BLACK)

#create list of buttons
buttonsList = ["Start", "Exit"]
restartList = ["Restart", "Exit"]

#create a button box that promts the user to start or exit game. if user clicks start, start the game
if e.boolbox("INSTRUCTIONS:\nUSE ARROW KEYS TO PILOT SHIP AND SPACE TO SHOOT PROJECTILES AND DESTROY ENEMY SHIPS. DO NOT LET THE ENEMIES GET PAST YOU AND DO NOT CRASH INTO THEM. YOU WILL HAVE THE OPPORTUNITY TO GAIN LIVES BY COLLECTING FALLING HEARTS", "INVADERS OF SPACE", buttonsList):
    start = True

#while start = True
while (start):
    #while lives does not = 0
    while (lives != 0):        
        #set fps
        clock.tick(60)

        #draw background
        screen.blit(bg, (0,0))

        #draw score text
        screen.blit(Score, (0,5))
        screen.blit(stext, (155, 3))

        #draw # of lives
        displayLives(lives)

        #check if there are any hearts on screen and if the player has lost a life
        if (len(hearts) == 0 and lives != 3):
            #start the timer and round it to seconds.
            timer += clock.get_time()
            heartTimer = round(timer/1000)

        #spawn in hearts if the timer exceeds a certain value and the amount of additional hearts  on screen is not one
        if (heartTimer > r.randint(5, 20) and len(hearts) != 1):
            heart = gainLives(r.randint(100, width - 100),r.randint(-1200, -200), extraHeart)
            hearts.append(heart)
        
        #spawn in hearts and check for collisions or if it went off screen. 
        for heart in hearts:
            #draw and move enemies on screen
            heart.draw()
            heart.move(heartVel)
            #check if heart is off screen
            if heart.y > 450:
                #remove heart from screen
                hearts.remove(heart)
            #check if player collided with heart
            if (pygame.sprite.collide_rect(player, heart)):
                #add one to lives and remove heart from screen. reset timers
                hearts.remove(heart)
                lives += 1
                timer = 0
                heartTimer = 0
        
        
        
        
        
        
        
        #if there are no enemies left, change level and spawn in more. 
        if (len(enemyList) == 0):
            level += 1
            enemyNumber += 1
            #spawn in enemies at random positions
            for i in range (enemyNumber):
                enemy = Enemy(r.randint(100, width - 100),r.randint(-1200, -200), enemyship)
                enemyList.append(enemy)
    
        #spawn in enemies
        for enemy in enemyList:
            enemy.draw()
            enemy.move(enemyVel)
            if (enemy.y > height):
                enemyList.remove(enemy)
                lives -= 1
            #check collisions between player and enemy ships
            if (pygame.sprite.collide_rect(player, enemy)):
                lives -= 1
                enemyList.remove(enemy)
        
        #spawn in projectiles
        for proj in projectiles:
            proj.draw()
            proj.move(projVel)
            
            #check if projectile is off screen
            if (proj.y <= 0):
                #remove projectile
                projectiles.remove(proj)
            
            #for every enemy that is on screen
            for enemy in enemyList:
                #check collisions between projectiles and enemies
                if (pygame.sprite.collide_rect(proj, enemy)):
                    #remove projectiles and enmies if collision is detected
                    enemyList.remove(enemy)
                    projectiles.remove(proj)
                    #change score
                    score += 1
                    stext = font.render(str(score), True, WHITE, BLACK)
        #draw player ship
        player.draw()

        #check for events
        event = pygame.event.poll()

        #if X is clicked, quit the program
        if (event.type == pygame.QUIT):
            start = False
            break

        #get keys pressed
        keys = pygame.key.get_pressed()

        #if key right arrow is pressed, and ship is not going off screen, move ship to the right
        if (keys[pygame.K_RIGHT] and player.x < width - 50):
            player.x += playerVel

        #if key left arrow is pressed, and ship is not going off screen, move ship to the left
        if (keys[pygame.K_LEFT] and player.x > 0):
            player.x -= playerVel

        #if key up arrow is pressed, and ship is not going off screen, move ship up
        if (keys[pygame.K_UP] and player.y > 0):
            player.y -= playerVel
        
        #if key down arrow is pressed, and ship is not going off screen, move ship down
        if (keys[pygame.K_DOWN] and player.y < height - 50):
            player.y += playerVel

        #if space is pressed
        if (keys[pygame.K_SPACE]):
            #check how many projetiles are on screen,if the number of projectiles does not = 1
            if (len(projectiles) != 1):
                #spawn in a projectile
                proj = Proj(player.x + 24.1, player.y, projectile)
                projectiles.append(proj)
        
        #update the display
        pygame.display.flip()
    
    #if no more lives remain
    if (lives == 0):
        #display the lives
        displayLives(lives)
        
        #update the display
        pygame.display.flip()

        #if score is greater than highscore
        if score > highscore:
            #update highscore to highest score
            highscore = score
            #open the highscore text file and write the new highscore into text file
            hs = open("Highscores.txt", "w")
            hs.write("Highscore: " + str(highscore))
        
        #close the file
        hs.close()
        
        #prompt user to restart game or exit game
        if e.boolbox("YOU'VE LOST ALL YOUR LIVES. YOUR SCORE WAS "+ str(score) + "\nWOULD YOU LIKE TO RESTART?", "INVADERS OF SPACE", restartList):
            #if user clicks restart, set variables back to original values
            lives = 3
            enemyNumber = 0
            level = 0
            score = 0
            enemyList.clear()
            projectiles.clear()
            stext = font.render(str(score), True, WHITE, BLACK)
            player.x = 375
            player.y = 325
            timer = 0
            heartTimer = 0
        else:
            #if user clicks exit, break the program
            break