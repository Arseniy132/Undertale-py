import pygame
from time import sleep
from random import randint
from pygame import transform

pygame.init()

font = pygame.font.Font("determination-extended.ttf", 40)
font_s = pygame.font.Font("determination-extended.ttf", 12)

screen = pygame.display.set_mode((1366, 768), )
clock = pygame.time.Clock()

pygame.mixer.init()
Ooo = pygame.mixer.Sound("Ooo.wav")

def attack():
    Attack = randint(1, 5)
    if Attack==1:
        while leg_1.rect.y  != 500:
            leg_1.height += 5
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
            clock.tick(60)

class Area:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def fill(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, color=None):
        Area.__init__(self, x, y, width, height, color)
        self.image = pygame.image.load(filename)

    def draw_picture(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, speed, width, height):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(pygame.image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Frisk(GameSprite):
    def __init__(self, filename, x, y, speed, width, height):
        GameSprite.__init__(self, filename, x, y, speed, width, height)
        self.counter = 0

    def anim(self, type):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.type = "walk"
        else:
            self.type = "stand"

        if self.type == "walk":
            self.counter += 1
            if self.counter >= 0 and self.counter < 10:
                self.image = transform.scale(pygame.image.load("STAND\LEFT.png"), (self.width, self.height))

            elif self.counter >= 10 and self.counter < 20:
                self.image = transform.scale(pygame.image.load("STAND\STAND.png"), (self.width, self.height))

            elif self.counter >= 20 and self.counter < 30:
                self.image = transform.scale(pygame.image.load("STAND\RIGHT.png"), (self.width, self.height))

            elif self.counter >= 30 and self.counter < 40:
                self.image = transform.scale(pygame.image.load("STAND\STAND2.png"), (self.width, self.height))

            if self.counter > 40:
                self.counter = 0
        elif self.type == "stand":
            self.image = transform.scale(pygame.image.load("STAND\STAND.png"), (self.width, self.height))


class Heart(GameSprite):
    def __init__(self, filename, x, y, speed, width, height):
        GameSprite.__init__(self, filename, x, y, speed, width, height)
        self.counter = 0

    def move(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if not self.check(self.rect.x, self.rect.y - self.speed, walls):
                self.rect.y -= self.speed
        if keys[pygame.K_s]:
            if not self.check(self.rect.x, self.rect.y + self.speed, walls):
                self.rect.y += self.speed
        if keys[pygame.K_a]:
            if not self.check(self.rect.x - self.speed, self.rect.y, walls):
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
            if not self.check(self.rect.x + self.speed, self.rect.y, walls):
                self.rect.x += self.speed

    def check(self, x, y, walls):
        wall_touch = []
        tmp_area = pygame.Rect(x, y, self.width, self.height)
        for wall in walls:
            wall.reset()
            wall_touch.append(wall.rect.colliderect(tmp_area))
        return True in wall_touch


leg_1 = GameSprite("ATTACKS/Leg.png", 58, 47, 0, 361, 300)
leg_2 = GameSprite("ATTACKS/Leg.png", 500, 500, 0, 361, 800)
leg_3 = GameSprite("ATTACKS/Leg.png", 500, 500, 0, 361, 800)
legs = [leg_1, leg_2, leg_3]

putin_map = GameSprite("putin_map.png", 647, 222, 0, 21, 21)
bg = GameSprite("bg.png", 0, 0, 0, 1366, 768)
putin = GameSprite("putin.png", 200, 530, 0, 230, 219)
Dialogue = GameSprite("dialogue.png", 110, 500, 0, 1150, 280)
Frisk = Frisk("Stand/STAND.png", 650, 700, 2, 57, 90)
black = GameSprite("black.png", 0, 0, 0, 1366, 768)
transparent = GameSprite("black.png", 0, 0, 0, 0, 0)

chapter = "menu"
BG_MNU = GameSprite("logo.png", 0, 0, 0, 1366, 768)

heart = Heart("heart.png", 500, 450, 5, 66, 66)
battle_screen = GameSprite("battle.jpg", 0, 0, 0, 1366, 768)

wall1 = GameSprite("wall.png", 0, 0, 0, 56, 1000)
wall2 = GameSprite("wall.png", 0, 0, 0, 1366, 45)
wall3 = GameSprite("wall.png", 1312, 0, 0, 58, 1000)
wall4 = GameSprite("wall.png", 0, 610, 0, 1366, 45)
walls = [wall1, wall2, wall3, wall4]

while True:
    if chapter == "menu":
        BG_MNU.reset()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    chapter = "corridor"

            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
        clock.tick(60)

    if chapter == "corridor":

        bg.reset()
        putin_map.reset()
        Frisk.reset()

        Ooo.play()

        enter = font_s.render("(Press enter)", True, "white")
        p_text = font.render("Вы что здесь делаете!?", True, "white")
        esc = font_s.render("(press Esc to get out)", True, "black")
        screen.blit(esc, (0, 0))

        if Frisk.rect.y != 500:
            Frisk.anim(type)
        else:
            Dialogue.reset()
            putin.reset()
            screen.blit(p_text, (500, 560))
            screen.blit(enter, (550, 660))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        i = 1
                        while i != 5:
                            black.reset()
                            sleep(0.2)
                            transparent.reset()
                            sleep(0.2)
                            i += 1
                            pygame.display.update()
                            clock.tick(60)
                        chapter = "battle"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    chapter = "menu"
                if event.key == pygame.K_UP:
                    chapter = "battle"

        pygame.display.update()
        clock.tick(60)

    if chapter == "battle":
        Ooo.stop()
        esc = font.render("(press Esc to get out)", True, "white")
        screen.blit(esc, (0, 0))

        for wall in walls:
            wall.reset()

        battle_screen.reset()
        heart.reset()
        heart.move(walls)
        leg_1.reset()
        attack()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
        clock.tick(60)
