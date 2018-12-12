
import random
import json
from pygame.locals import *
import os
import pygame
import pygameMenu
from pygameMenu.locals import *

WIDTH = 900
HEIGHT = 700
FPS = 60

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Defender")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def pontuacao(surf, text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True, (255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.dificuldade =1
    def update(self):
        self.score += 1
        if self.score ==10:
            self.dificuldade = 4
            print(self.dificuldade)
        if self.score ==30:
            self.dificuldade = 6
            print(self.dificuldade)
        if self.score == 70:
            self.dificuldade = 8
            print(self.dificuldade)
        if self.score == 100:
            self.dificuldade = 10
            print(self.dificuldade)
        if self.score == 130:
            self.dificuldade = 14
            print(self.dificuldade)
        if self.score == 200:
            self.dificuldade = 18
            print(self.dificuldade)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('oldplayer.PNG')
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.col0 = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        pts = Score()
        if pts.score == 200:
            if self.col0 == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.col0 = 100
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        if self.col0 > 0 :
            self.col0 -=1

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('inimigo.PNG')
        self.image= pygame .transform.scale(self.image,(120,80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100 , 800)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        if self.rect.x < WIDTH/2:
            self.speedx = random.randrange(0, 1)
        else:
            self.speedx = random.randrange(-1, 0)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT - 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('tiro.PNG')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

audio=pygame.mixer.Sound('boom.wav')
audio_tiro= pygame.mixer.Sound('disparo.wav')
audio_jogo = pygame.mixer.Sound('tema.wav')
audio_gameOver = pygame.mixer.Sound('gameOver.wav')
font = pygame.font.get_default_font()

font2= pygame.font.SysFont(font,70)
pygame.font.init()
try:
    abre=open('pontuação.json','r')
    Mpts = json.load(abre)
    abre.close()
except:
    Mpts = 0

coracao = pygame.image.load('vida.PNG')
coracao = pygame.transform.scale(coracao,(30,20))

bg = pygame.image.load('fundo.PNG')
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

all_sprites = pygame.sprite.Group()

mobs = pygame.sprite.Group()

bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
def jogo():
    vida =3
    score = 0
    pts = Score()

    running = True

    col =0
    col2 =0

    audio_jogo.play(3)

    while running:
        if col2 == 0:
                for i in range(pts.dificuldade):
                    m = Mob()
                    all_sprites.add(m)
                    mobs.add(m)
                    mobs.draw(screen)
                col2 = 100
                if pts.dificuldade == 8:
                    col2 = 150
                if pts.dificuldade == 14:
                    col2 = 200

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pts.score == 200:
                pygame.key.set_repeat(10,50)
                press = pygame.key.get_pressed()

                if col == 0:
                    if press[pygame.K_SPACE]:
                        audio_tiro.play()
                        player.shoot()
                        col = 1000
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    audio_tiro.play()
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            pts.update()
            score = pts.score

        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            audio.play()
        if hits:
            vida -= 1
        if vida == 0:
            if score > Mpts:
                abre = open('pontuação.json','w')
                abre.write(str(score))
                abre.close()
            running = False
            audio_jogo.stop()
            audio_gameOver.play(3)
            show_go_screen(score,Mpts,)

        if col >0:
            col -=0.1

        if col2 >0:
            col2 -= 1
        screen.blit(bg,(0,0))
        screen.blit(coracao,(WIDTH/2 -400, 10))
        all_sprites.draw(screen)
        pontuacao(screen,"PONTUAÇÃO: ", 18, WIDTH/2 -100, 10)
        pontuacao(screen, str(score),18,WIDTH/2 -30,10 )
        pontuacao(screen,str(vida), 18, WIDTH/2 -360, 10)
        pontuacao(screen,"MELHOR PONTUAÇÃO:", 18, WIDTH/2 +250, 10)
        pontuacao(screen,str(Mpts), 18, WIDTH/2 +380, 10)
        pygame.display.flip()
	
    pygame.quit()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_gameOver(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen(score,Mpts):

    screen.fill((0,0,0))
    draw_gameOver(screen, 'Game Over',64,WIDTH/2,HEIGHT/4)
    draw_text(screen, 'Pontuação',25,WIDTH/2 -100,HEIGHT/4 + 100)
    draw_text(screen, str(score),25,WIDTH/2 -100,HEIGHT/4 + 150)
    if score > Mpts:
        draw_text(screen, 'Nova Melhor Pontuação',25,WIDTH/2 +100,HEIGHT/4 + 100)
        draw_text(screen, str(score),25,WIDTH/2 +100,HEIGHT/4 + 150)
    else:
        draw_text(screen, 'Melhor Pontuação',25,WIDTH/2 +100,HEIGHT/4 + 100)
        draw_text(screen, str(Mpts),25,WIDTH/2 +100,HEIGHT/4 + 150)
    draw_text(screen,  'Precione Esc para sair!',18,WIDTH/2,HEIGHT/4 + 450)
    draw_text(screen,  'Desenvolvido por: Erick Nagoski e Gabriel Londre',18,WIDTH/2 + 250,HEIGHT/4 + 500)
    pygame.display.flip()
    true = True
    while true:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

COLOR_BACKGROUND = (0, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (3, 64, 137)
WINDOW_SIZE = (WIDTH, HEIGHT)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('MENU INICIAL')
clock = pygame.time.Clock()
dt = 1 / FPS


def play_function():
    jogo()
    main_menu.disable()
    main_menu.reset(1)

    while True:
        clock.tick(60)

        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    return

        main_menu.mainloop(events)
        pygame.display.flip()

def main_background():
    surface.fill(COLOR_BACKGROUND)

# PLAY MENU
play_menu= pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1]*1),
                            menu_width=int(WINDOW_SIZE[0] *1),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='The defender',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

play_menu.add_option('Iniciar', play_function)
play_menu.add_option('Retornar ao menu principal', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 1),
                            menu_width=int(WINDOW_SIZE[0] * 1),

                            option_shadow= False,
                            title='The defender',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.add_option('Jogar', play_menu)
main_menu.add_option('Sair', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
def menu():
		
	while True:

    # Tick
		clock.tick(60)

    # Application events
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				exit()

    # Main menu
		main_menu.mainloop(events)

    # Flip surface
		pygame.display.flip()

menu()
