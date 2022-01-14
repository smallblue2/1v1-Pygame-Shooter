#!/usr/bin/env python3

# Imports
from os import X_OK
import pygame
from pygame import key
import random
pygame.font.init()
pygame.mixer.init()

# Global Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
TIMER = 0
MAX_BULLETS = 5
P_UP_SPAWN_RATE = 600
P_UP_DURATION = 1
FONT = pygame.font.Font('assets/Voyager Heavy.otf', 20)

# Loading Shapes
midline = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

# Loading Assets
bg = pygame.image.load("assets/space.png")
spaceship1_image = pygame.image.load("assets/player1.png")
spaceship2_image = pygame.image.load("assets/player2.png")
bullet_image = pygame.image.load("assets/bullet.png")
speed_up_image = pygame.image.load("assets/speed_powerup.png")
health_up_image = pygame.image.load("assets/health_powerup.png")
p1_bullet_sound = pygame.mixer.Sound("assets/ship1sound.wav")
p2_bullet_sound = pygame.mixer.Sound("assets/ship2sound.wav")
hit_sound = pygame.mixer.Sound("assets/hitsound.wav")

# Game Objects
class P1:
	def __init__(self, x, y):
		self.rect = pygame.Rect(x, y, 32, 32)
		self.x = x
		self.y = y
		self.w_pressed = False
		self.a_pressed = False
		self.s_pressed = False
		self.d_pressed = False
		self.speed = 3
		self.health = 5
		self.max_bullets = MAX_BULLETS
		self.bullets = []
		self.power_ups = []

	def update(self):
		self.velx = 0
		self.vely = 0
		# Checks key inputs and adjusts velocity
		if self.a_pressed and not self.d_pressed:
			if self.x - self.speed > 0:
				self.velx -= self.speed
		if self.d_pressed and not self.a_pressed:
			if self.x - self.speed < (WIDTH // 2) - 42:
				self.velx += self.speed
		if self.w_pressed and not self.s_pressed:
			if self.y + self.speed > 0:			
				self.vely -= self.speed
		if self.s_pressed and not self.w_pressed:
			if self.y - self.speed < HEIGHT - 32:
				self.vely += self.speed
		# Update's player's position
		self.x += self.velx
		self.y += self.vely
		self.rect = pygame.Rect(self.x, self.y, 32, 32)



class P2:
	def __init__(self, x, y):
		self.rect = pygame.Rect(x, y, 32, 32)
		self.x = x
		self.y = y
		self.up_pressed = False
		self.left_pressed = False
		self.down_pressed = False
		self.right_pressed = False
		self.speed = 3
		self.health = 5
		self.max_bullets = MAX_BULLETS
		self.bullets = []
		self.power_ups = []

	def update(self):
		self.velx = 0
		self.vely = 0
		# Checks key inputs and adjusts velocity
		if self.left_pressed and not self.right_pressed:
			if self.x - self.speed > (WIDTH / 2) + 5:
				self.velx -= self.speed
		if self.right_pressed and not self.left_pressed:
			if self.x + self.speed < WIDTH - 32:
				self.velx += self.speed
		if self.up_pressed and not self.down_pressed:
			if self.y + self.speed > 0:
				self.vely -= self.speed
		if self.down_pressed and not self.up_pressed:
			if self.y - self.speed < HEIGHT - 32:
				self.vely += self.speed
		# Updates player's position
		self.x += self.velx
		self.y += self.vely
		self.rect = pygame.Rect(self.x, self.y, 32, 32)

class BULLET:
	speed = 5
	def __init__(self, side, player):
		if side == 1:
			p1_bullet_sound.play()
			self.x = player.x + 34
			self.y = player.y + 8
			self.rect = pygame.Rect(self.x, self.y, 16, 16)
		elif side == 2:
			p2_bullet_sound.play()
			self.x = player.x - 16
			self.y = player.y + 8
			self.rect = pygame.Rect(self.x, self.y, 16, 16)

class POWER_UP:
	def __init__(self, x, y, type, TIMER):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, 15, 15)
		self.type = type
		self.clock = 0
		self.expire = TIMER + (P_UP_DURATION * 300)
	
	def reset_expiry(self, multiplier):
		self.expire = TIMER + multiplier * (P_UP_DURATION * 300)

# Draw Loop
def draw_window(p1, p2, power_ups):
	WIN.blit(bg, (0,0))
	pygame.draw.rect(WIN, (255, 255, 255), midline)
	p1_health_text = FONT.render("Health: %i" % (p1.health), 1, (255, 255, 255))
	p2_health_text = FONT.render("Health: %i" % (p2.health), 1, (255, 255, 255))
	WIN.blit(spaceship1_image, (p1.x, p1.y))
	WIN.blit(spaceship2_image, (p2.x, p2.y))
	for bullet in p1.bullets:
		WIN.blit(pygame.transform.rotate(bullet_image, -90), (bullet.x, bullet.y))
	for bullet in p2.bullets:
		WIN.blit(pygame.transform.rotate(bullet_image, 90), (bullet.x, bullet.y))
	for p_up in power_ups:
		if p_up.type == 1:
			WIN.blit(speed_up_image, (p_up.x, p_up.y))
		if p_up.type == 2:
			WIN.blit(health_up_image, (p_up.x, p_up.y))
	WIN.blit(p1_health_text, (32, 10))
	WIN.blit(p2_health_text, (WIDTH - 32 - p1_health_text.get_width(), 10))
	pygame.display.update()

# Main Loop
def main():
	power_ups = []
	clock = pygame.time.Clock()
	run = True

	p1 = P1(50, HEIGHT/2)
	p2 = P2(WIDTH - 80, HEIGHT//2)

	while run:
		clock.tick(FPS)
		global TIMER
		TIMER += 1
		# EVENT CHECKER
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			# Key Down Checks
			if event.type == pygame.KEYDOWN:
				# Player 1 Key Checks
				if event.key == pygame.K_a:
					p1.a_pressed = True
				if event.key == pygame.K_d:
					p1.d_pressed = True
				if event.key == pygame.K_w:
					p1.w_pressed = True
				if event.key == pygame.K_s:
					p1.s_pressed = True
				if event.key == pygame.K_SPACE :
					if len(p1.bullets) < p1.max_bullets:
						p1b = BULLET(1, p1)
						p1.bullets.append(p1b)
				# Player 2 Key Checks
				if event.key == pygame.K_LEFT:
					p2.left_pressed = True
				if event.key == pygame.K_RIGHT:
					p2.right_pressed = True
				if event.key == pygame.K_UP:
					p2.up_pressed = True
				if event.key == pygame.K_DOWN:
					p2.down_pressed = True
				if event.key == pygame.K_RCTRL:
					if len(p2.bullets) < p2.max_bullets:
						p2b = BULLET(2, p2)
						p2.bullets.append(p2b)
	
			# Key Up Checks
			if event.type == pygame.KEYUP:
				# Player 1 Key Checks
				if event.key == pygame.K_a:
					p1.a_pressed = False
				if event.key == pygame.K_d:
					p1.d_pressed = False
				if event.key == pygame.K_w:
					p1.w_pressed = False
				if event.key == pygame.K_s:
					p1.s_pressed = False
				# Player 2 Key Checks
				if event.key == pygame.K_LEFT:
					p2.left_pressed = False
				if event.key == pygame.K_RIGHT:
					p2.right_pressed = False
				if event.key == pygame.K_UP:
					p2.up_pressed = False
				if event.key == pygame.K_DOWN:
					p2.down_pressed = False
		
		# Power-up Spawner
		chance = random.randint(0, P_UP_SPAWN_RATE)
		if chance == 0:
			# Decides side to spawn at
			side = random.randint(1,2)
			type = random.randint(1,2)
			if side == 1:
				x = random.randint(0, (WIDTH // 2) - 15)
				y = random.randint(0, HEIGHT - 15)
				p_up = POWER_UP(x, y, type, TIMER)
				power_ups.append(p_up)
			else:
				x = random.randint((WIDTH // 2) + 15, WIDTH)
				y = random.randint(0, HEIGHT - 15)
				p_up = POWER_UP(x, y, type, TIMER)
				power_ups.append(p_up)

		# Checkes players' health
		if p1.health == 0 or p2.health == 0:
			run = False
			if p1.health < p2.health:
				winner = "p2"
			else:
				winner = "p1"
			for bullet in p1.bullets:
				del bullet
			for bullet in p2.bullets:
				del bullet
			del p1
			del p2
			gameover(winner)

		# UPDATE OBJECTS	
		p1.update()
		p2.update()
		# HANDLE OBJECTS
		bullet_handler(p1, p2)
		power_up_handler(p1, p2, power_ups)
		# UPDATE WINDOW
		draw_window(p1, p2, power_ups)

# Bullet Handler
def bullet_handler(p1, p2):
	# Moving p1's bullets
	for bullet in p1.bullets:
		bullet.x += BULLET.speed
		bullet.rect = pygame.Rect(bullet.x, bullet.y, 16, 16)
		# Checking p1's bullet's collision
		if pygame.Rect.colliderect(bullet.rect, p2.rect):
			hit_sound.play()
			p1.bullets.remove(bullet)
			del bullet
			p2.health -= 1
			print("HIT P2")
		elif bullet.x > WIDTH:
			p1.bullets.remove(bullet)
			del bullet
	# Moving p2's bullets
	for bullet in p2.bullets:
		bullet.x -= BULLET.speed
		bullet.rect = pygame.Rect(bullet.x, bullet.y, 16, 16)
		# Checking p2's bullet's collision
		if pygame.Rect.colliderect(bullet.rect, p1.rect):
			hit_sound.play()
			p2.bullets.remove(bullet)
			del bullet
			p1.health -= 1
			print("HIT P1")
		elif bullet.x < 0:
			p2.bullets.remove(bullet)
			del bullet

# Handler Function For Power-ups
def power_up_handler(p1, p2, power_ups):
	
	# Checking Power-up Collision for both players
	for power_up in power_ups:
		# Checks power-up's expiry
		if power_up.expire < TIMER:
			power_ups.remove(power_up)
			del power_up
			continue
		# Checks collision with p1
		if pygame.Rect.colliderect(power_up.rect, p1.rect):
			# Modify's stats and appends power-up to player attribute
			if power_up.type == 1:
				p1.speed *= 1.5
				power_up.reset_expiry(2)
				p1.power_ups.append(power_up)
				power_ups.remove(power_up)
			if power_up.type == 2:
				p1.health += 1
				power_ups.remove(power_up)
				del power_up
		# Checks collision with p2
		elif pygame.Rect.colliderect(power_up.rect, p2.rect):
			# Modify's stats and appends power-up to player attribute
			if power_up.type == 1:
				p2.speed *= 1.5
				power_up.reset_expiry(2)
				p2.power_ups.append(power_up)
				power_ups.remove(power_up)
			if power_up.type == 2:
				p2.health += 1
				power_ups.remove(power_up)
				del power_up
	
	# Checks p1's power-up expiries
	for power_up in p1.power_ups:
		if power_up.expire < TIMER:
			if power_up.type == 1:
				p1.speed /= 1.5
			p1.power_ups.remove(power_up)
			del power_up
	
	# Checks p2's power-up expiries
	for power_up in p2.power_ups:
		if power_up.expire < TIMER:
			if power_up.type == 1:
				p2.speed /= 1.5
			p2.power_ups.remove(power_up)
			del power_up
			
			

# Game Over Function
def gameover(winner):
	# Display the winner
	FONT = pygame.font.Font('assets/Voyager Heavy.otf', 50)
	winning_text = FONT.render("%s Wins!" % (winner), 1, (255, 255, 255))
	WIN.fill((0, 0, 0))
	WIN.blit(winning_text, (((WIDTH // 2) - (winning_text.get_width() // 2)), HEIGHT // 2))
	pygame.display.update()
	# Checks for restart or for exit
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main()

# Starts the script
if __name__ == "__main__":
	main()