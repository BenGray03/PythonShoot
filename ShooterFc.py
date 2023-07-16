import pygame
import time
import math
import random
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter FC")

FONT = pygame.font.SysFont("comicsans", 16)

RED = (255, 24, 24)
LIGHTGREEN = (144, 238, 144)
WHITE = (255, 255, 255)

class Enemy:
    def __init__(self, x, y, radius, Target, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.Target = Target
        self.speed = speed
        self.health = radius*10
        self.alive = True
    
    def move(self):
        dx = self.Target.x - self.x
        dy = self.Target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance  
            self.x += dx_normalized * self.speed
            self.y += dy_normalized * self.speed
    
    def drawEnemy(self, win):
        x = self.x + WIDTH/2
        y = self.y + HEIGHT/2
        pygame.draw.circle(win, RED, (x, y), self.radius)
    
class Player:
    def __init__(self, x, y, health, speed):
       self.x = x
       self.y = y
       self.health = health
       self.speed = speed


    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def drawPlayer(self, win):
        x = self.x + WIDTH/2
        y = self.y + HEIGHT/2 
        pygame.draw.circle(win, LIGHTGREEN, (x, y), 10)
    

class Bullet():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 5
    
    def move(self):
        if self.dx == 0 and self.dy == 0:
            self.dx = 1
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def drawBullet(self, win):
        x = self.x + WIDTH / 2
        y = self.y + HEIGHT / 2
        pygame.draw.circle(win, WHITE, (x, y), 2)
    
    def checkHit(self, enemies):
        for enemy in enemies:
            dx = self.x - enemy.x
            dy = self.y - enemy.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= (enemy.radius + 2):
                enemy.health -= 10
                if enemy.health <= 0:
                    enemy.alive = False
                return True

        return False

def spawnEnemies(wave, enemies, player):
    i = 0
    while i <= wave:
        x = random.randint(-400, 400)
        y = random.randint(-400, 400)
        
        enemy = Enemy()
        enemies.append()
        i += 1


def main():
    running = True
    clock = pygame.time.Clock()
    
    user = Player(0, 0, 100, 3)
    enemy = Enemy(-200, -200, 10, user, 1)
    bullets = []  # Store the bullets fired by the player
    enemies = []  #store list of enemies
    keys_pressed = set()  # Track the keys currently being held down

    enemies.append(enemy)
    while running:
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():  # check events
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)  # Add pressed key to the set
                if event.key == pygame.K_SPACE:
                    # Create a bullet and add it to the bullets list
                    bullet = Bullet(user.x, user.y, dx, dy)  # Upward direction initially
                    bullets.append(bullet)
            if event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)  # Remove released key from the set

        # Check the keys being held down for continuous movement
        dx = 0
        dy = 0
        if pygame.K_w in keys_pressed:
            dy -= 1  # Move up
        if pygame.K_s in keys_pressed:
            dy += 1  # Move down
        if pygame.K_a in keys_pressed:
            dx -= 1  # Move left
        if pygame.K_d in keys_pressed:
            dx += 1  # Move right
        user.move(dx, dy)  # Pass the movement vector to the player's move method
        healthm = "HP: {}".format(user.health)
        hp = FONT.render(healthm, 1, WHITE)
        WIN.blit(hp, 100, 100)

        # Update and draw the bullets
        for bullet in bullets:
            bullet.move()
            if bullet.checkHit(enemies):
                bullets.remove(bullet)
            bullet.drawBullet(WIN)
            # Remove the bullet if it goes off-screen
            if bullet.y < -410 or bullet.y > HEIGHT/2 or bullet.x < -410 or bullet.x > WIDTH/2:
                bullets.remove(bullet)

        # Update and draw enimies
        for enemy in enemies:
            if enemy.alive == False:
                enemies.remove(enemy)

            enemy.move()
            enemy.drawEnemy(WIN)

        user.drawPlayer(WIN)

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()

main()