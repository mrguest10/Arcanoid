import pygame


BLACK = (0, 0, 0)
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=(0, 0, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def new_color(self, color):
        self.fill_color = color

    def draw_rectangle(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

class Picture(Area):
    def __init__(self, file_name, x=0, y=0, width=10, height=10, color=(0, 0, 255)):
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        self.image = pygame.image.load(file_name)

    def draw(self, shift_x=0, shift_y=0):
        self.draw_rectangle()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self, text='CLICK', fsize=12, text_color=BLACK):
        self.text = text
        self.image = pygame.font.Font(None, fsize).render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.draw_rectangle()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

pygame.init()
window = pygame.display.set_mode((500, 500))
window.fill((173, 216, 230))
clock = pygame.time.Clock()

platform = Picture('platform.png', 225, 575, 100, 40, (173, 216, 230))
platform.draw()
ball = Picture('ball.png', 245, 515, 50, 50, (173, 216, 230))
ball.draw()

monsters = []
start_x = 0
start_y = 0
n = 9
for j in range(3):
    x = start_x + (27*j)
    y = start_y + (50*j)
    for i in range(n):
        enemy = Picture('enemy.png', x, y, 50, 50, (173, 216, 230))
        monsters.append(enemy)
        x += 55
    n -= 1

move_right = False
move_left = False
speed_x = 3
speed_y = 3
platform_y = 575
back = (173, 216, 230)
while True:
    window.fill((173, 216, 230))
    ball.draw()
    ball.rect.x += speed_x
    ball.rect.y += speed_y
    if ball.colliderect(platform.rect):
        speed_y *= -1
        ball.rect.bottom = platform.rect.top
    if ball.rect.y < 0:
        speed_y *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1
    if ball.rect.y > (platform_y + 20):
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        break
    for enemy in monsters:
        enemy.draw()
        if enemy.rect.colliderect(ball.rect):
            monsters.remove(enemy)
            enemy.draw_rectangle()
            speed_y *= -1
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        break
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False
    if move_right == True:
        platform.rect.x += 3
    elif move_left == True:
        platform.rect.x -= 3
    platform.draw()
    clock.tick(40)
    pygame.display.update()
pygame.display.update()
