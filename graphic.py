import pygame
import os
import time
import threading
from playsound import playsound

pygame.init()
pygame.font.init()

dis_width = 1000
dis_height = 600
fps = 60
speed = 5
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

p_w, p_h = 120, 120
p_one_x = dis_width * 0.33
p_two_x = dis_width * 0.5

game_dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Fancy Fencing')
clock = pygame.time.Clock()

p_one_img = pygame.image.load(os.path.join('img', 'p_one.png'))
p_one = pygame.transform.scale(p_one_img, (p_w, p_h))
p_one_attack_img = pygame.image.load(os.path.join('img', 'p_one_attack.png'))
p_one_attack = pygame.transform.scale(p_one_attack_img, (p_w, p_h))
p_one_block_img = pygame.image.load(os.path.join('img', 'p_one_block.png'))
p_one_block = pygame.transform.scale(p_one_block_img, (p_w, p_h))

p_two_img = pygame.image.load(os.path.join('img', 'p_two.png'))
p_two = pygame.transform.scale(p_two_img, (p_w, p_h))
p_two_attack_img = pygame.image.load(os.path.join('img', 'p_two_attack.png'))
p_two_attack = pygame.transform.scale(p_two_attack_img, (p_w, p_h))
p_two_block_img = pygame.image.load(os.path.join('img', 'p_two_block.png'))
p_two_block = pygame.transform.scale(p_two_block_img, (p_w, p_h))

pl_g_img = pygame.image.load(os.path.join('img', 'pl_g.jpg'))

controls_img = pygame.image.load(os.path.join('img', 'controls.png'))

font = pygame.font.Font('freesansbold.ttf', (30))

# left_border = pygame.Rect(130, 0, 10, dis_height)
# right_border = pygame.Rect(dis_width - 130, 0, 10, dis_height)
p_one_score = 0
p_two_score = 0

p_one_attacking = False
p_one_blocking = False

p_two_attacking = False
p_two_blocking = False

# help screen


def help_screen():
    help = True
    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_dis.fill(black)
        pl_g()
        # title
        text = font.render('Fancy Fencing', True, white, black)
        textRect = text.get_rect()
        textRect.center = (130, 30)
        game_dis.blit(text, textRect)

        # start button
        text = font.render('Press Space to Play', True, white, black)
        textRect = text.get_rect()
        textRect.center = (dis_width-170, 30)
        game_dis.blit(text, textRect)

        # help on controls
        game_dis.blit(controls_img, ((dis_width//2) - 200, 100))

        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            help = False
            game_loop()


# function to display the menu screen
def menu_screen():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_dis.fill(black)
        pl_g()
        # title
        text = font.render('Fancy Fencing', True, white, black)
        textRect = text.get_rect()
        textRect.center = (dis_width // 2, dis_height // 2)
        game_dis.blit(text, textRect)

        # start button
        text = font.render('Press Space to Play', True, white, black)
        textRect = text.get_rect()
        textRect.center = (dis_width // 2, dis_height // 2 + 50)
        game_dis.blit(text, textRect)

        # help button
        text = font.render('Press H for Help', True, black, white)
        textRect = text.get_rect()
        textRect.center = (dis_width // 2, dis_height // 2 + 100)
        game_dis.blit(text, textRect)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu = False
            game_loop()

        if keys[pygame.K_h]:
            menu = False
            help_screen()


def pl_g():
    game_dis.blit(pl_g_img, (0, 300))


def resel_bool(boolem, sec=0.5):
    time.sleep(sec)
    if boolem:
        boolem = False
    return boolem


def play_sound(sound):
    if sound == "attack":
        playsound(os.path.join("sounds", "swod2.wav"))
    elif sound == "block":
        playsound(os.path.join("sounds", "swod1.wav"))


def draw_objects(p_one_win, p_two_win):
    global p_one_score, p_two_score, p_one_attacking, p_one_blocking,\
        p_two_attacking, p_two_blocking

    game_dis.fill(black)
    pl_g()

    # help text
    text = font.render('Press Escape for Help', True, white, black)
    textRect = text.get_rect()
    textRect.center = (dis_width - 170, 30)
    game_dis.blit(text, textRect)

    text = font.render(str(p_one_score), True, green, black)
    textRect = text.get_rect()
    textRect.center = (dis_width // 2 - 100, 20)
    game_dis.blit(text, textRect)
    text = font.render(str(p_two_score), True, red, black)
    textRect = text.get_rect()
    textRect.center = (dis_width // 2 + 100, 20)
    game_dis.blit(text, textRect)

    if p_one_attacking:
        game_dis.blit(p_one_attack, (p_one_win.x, p_one_win.y))
    elif p_one_blocking:
        game_dis.blit(p_one_block, (p_one_win.x, p_one_win.y))
    else:
        game_dis.blit(p_one, (p_one_win.x, p_one_win.y))

    if p_two_attacking:
        game_dis.blit(p_two_attack, (p_two_win.x, p_two_win.y))
    elif p_two_blocking:
        game_dis.blit(p_two_block, (p_two_win.x, p_two_win.y))
    else:
        game_dis.blit(p_two, (p_two_win.x, p_two_win.y))
    pygame.display.update()


mute = False


def loopBg():
    while not mute:
        playsound(os.path.join("sounds", "bg.mp3"))


loopBgThread = threading.Thread(target=loopBg)
loopBgThread.daemon = True
loopBgThread.start()


def game_loop():
    global p_one_score, p_two_score, p_one_attacking, p_one_blocking,\
        p_two_attacking, p_two_blocking

    game_over = False
    p_one_win = pygame.Rect(p_one_x, 240, p_w, p_h)
    p_two_win = pygame.Rect(p_two_x, 240, p_w, p_h)
    start_time = time.time()
    while not game_over:
        clock.tick(fps)
        play_time = "%.2f" % (time.time() - start_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    p_one_blocking = not p_one_blocking
                    p_one_attacking = False
                    if p_one_blocking:
                        play_sound("block")
                        p_one_win.x -= 20
                if event.key == pygame.K_z:
                    p_one_attacking = not p_one_attacking
                    p_one_blocking = False
                    if p_one_attacking:
                        play_sound("attack")
                        p_one_win.x += 20
                        if p_one_win.x > p_two_win.x + 2 and not p_two_blocking:
                            p_one_score += 1
                            p_one_win.x = p_one_x
                            p_two_win.x = p_two_x

                if event.key == pygame.K_UP:
                    p_two_attacking = not p_two_attacking
                    p_two_blocking = False
                    if p_two_attacking:
                        play_sound("attack")
                        p_two_win.x -= 20
                        if p_two_win.x < p_one_win.x + 2 and not p_one_blocking:
                            p_two_score += 1
                            p_one_win.x = p_one_x
                            p_two_win.x = p_two_x

                if event.key == pygame.K_DOWN:
                    p_two_blocking = not p_two_blocking
                    p_two_attacking = False
                    if p_two_blocking:
                        play_sound("block")
                        p_two_win.x += 20

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:  # Player 1 move left
            p_one_win.x -= speed

        if keys[pygame.K_d]:  # Player 1 move right
            p_one_win.x += speed

        if keys[pygame.K_LEFT]:  # Player 2 move left
            p_two_win.x -= speed

        if keys[pygame.K_RIGHT]:  # Player 2 move right
            p_two_win.x += speed

        # if keys[pygame.K_z]:  # Player 1 attack
        #     p_one_attacking = not p_one_attacking
        #     p_one_blocking = False
        #     if p_one_attacking:
        #         p_one_win.x += 10
        #         if p_one_win.x > p_two_win.x + 2 and not p_two_blocking:
        #             p_one_score += 1
        #             p_one_win.x = p_one_x
        #             p_two_win.x = p_two_x

        # if keys[pygame.K_s]:  # Player 1 block
        #     p_one_blocking = not p_one_blocking
        #     p_one_attacking = False
        #     if p_one_blocking:
        #         p_one_win.x -= 10

        # if keys[pygame.K_UP]:  # Player 2 attack
        #     p_two_attacking = not p_two_attacking
        #     p_two_blocking = False
        #     if p_two_attacking:
        #         p_two_win.x -= 10
        #         if p_two_win.x < p_one_win.x + 2 and not p_one_blocking:
        #             p_two_score += 1
        #             p_one_win.x = p_one_x
        #             p_two_win.x = p_two_x

        # if keys[pygame.K_DOWN]:  # Player 2 block
        #     p_two_blocking = not p_two_blocking
        #     p_two_attacking = False
        #     if p_two_blocking:
        #         p_two_win.x += 10

        if keys[pygame.K_ESCAPE]:
            menu = True
            menu_screen()
        # collision
        if p_one_win.x < 110:
            p_two_score += 1
            p_one_win.x = p_one_x - 100

        if p_two_win.x + p_w > dis_width - 100:
            p_one_score += 1
            p_two_win.x = p_two_x + 100

        # prevent players from passing each other
        if p_one_win.x + p_w > p_two_win.x + p_w:
            p_one_win.x = p_one_x

        if p_two_win.x < p_one_win.x:
            p_two_win.x = p_two_x

        draw_objects(p_one_win, p_two_win)
        pygame.display.update()


if __name__ == '__main__':
    menu_screen()
