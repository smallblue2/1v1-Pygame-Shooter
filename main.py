#!/usr/bin/env python3

# Imports
from os import X_OK
import pygame
from pygame import key
pygame.font.init()
pygame.mixer.init()

# Global Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
MAX_BULLETS = 4
FONT = pygame.font.Font('assets/Voyager Heavy.otf', 20)

# Loading Shapes
midline = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

# Loading Assets
bg = pygame.image.load("assets/space.png")
spaceship1_image = pygame.image.load("assets/player1.png")
spaceship2_image = pygame.image.load("assets/player2.png")
bullet_image = pygame.image.load("assets/bullet.png")
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

	def update(self):
		self.velx = 0
		self.vely = 0

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

	def update(self):
		self.velx = 0
		self.vely = 0
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


# Draw Loop
def draw_window(p1, p2, p1_bullets, p2_bullets):
	WIN.blit(bg, (0,0))
	pygame.draw.rect(WIN, (255, 255, 255), midline)
	p1_health_text = FONT.render("Health: %i" % (p1.health), 1, (255, 255, 255))
	p2_health_text = FONT.render("Health: %i" % (p2.health), 1, (255, 255, 255))
	WIN.blit(spaceship1_image, (p1.x, p1.y))
	WIN.blit(spaceship2_image, (p2.x, p2.y))
	for bullet in p1_bullets:
		WIN.blit(pygame.transform.rotate(bullet_image, -90), (bullet.x, bullet.y))
	for bullet in p2_bullets:
		WIN.blit(pygame.transform.rotate(bullet_image, 90), (bullet.x, bullet.y))
	WIN.blit(p1_health_text, (32, 10))
	WIN.blit(p2_health_text, (WIDTH - 32 - p1_health_text.get_width(), 10))
	pygame.display.update()

# Main Loop
def main():
	p1_bullets = []
	p2_bullets = []
	clock = pygame.time.Clock()
	run = True

	p1 = P1(50, HEIGHT/2)
	p2 = P2(WIDTH - 80, HEIGHT//2)

	while run:
		clock.tick(FPS)

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
				if event.key == pygame.K_LCTRL:
					if len(p1_bullets) <= MAX_BULLETS:
						p1b = BULLET(1, p1)
						p1_bullets.append(p1b)
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
					if len(p2_bullets) <= MAX_BULLETS:
						p2b = BULLET(2, p2)
						p2_bullets.append(p2b)
	
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

		if p1.health == 0 or p2.health == 0:
			run = False
			if p1.health < p2.health:
				winner = "p2"
			else:
				winner = "p1"
			del p1
			del p2
			for bullet in p1_bullets:
				del bullet
			for bullet in p2_bullets:
				del bullet
			gameover(winner)
		# UPDATE PLAYERS	
		p1.update()
		p2.update()
		bullet_handler(p1, p2, p1_bullets, p2_bullets)
		draw_window(p1, p2, p1_bullets, p2_bullets)

# Bullet Handler
def bullet_handler(p1, p2, p1_bullets, p2_bullets):
	for bullet in p1_bullets:
		bullet.x += BULLET.speed
		bullet.rect = pygame.Rect(bullet.x, bullet.y, 16, 16)
		if pygame.Rect.colliderect(bullet.rect, p2.rect):
			hit_sound.play()
			p1_bullets.remove(bullet)
			del bullet
			p2.health -= 1
			print("HIT P2")
		elif bullet.x > WIDTH:
			p1_bullets.remove(bullet)
			del bullet
	for bullet in p2_bullets:
		bullet.x -= BULLET.speed
		bullet.rect = pygame.Rect(bullet.x, bullet.y, 16, 16)
		if pygame.Rect.colliderect(bullet.rect, p1.rect):
			hit_sound.play()
			p2_bullets.remove(bullet)
			del bullet
			p1.health -= 1
			print("HIT P1")
		elif bullet.x < 0:
			p2_bullets.remove(bullet)
			del bullet

def gameover(winner):
	FONT = pygame.font.Font('assets/Voyager Heavy.otf', 50)
	winning_text = FONT.render("%s Wins!" % (winner), 1, (255, 255, 255))
	WIN.fill((0, 0, 0))
	WIN.blit(winning_text, (((WIDTH // 2) - (winning_text.get_width() // 2)), HEIGHT // 2))
	pygame.display.update()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main()

if __name__ == "__main__":
	main()