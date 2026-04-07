import math, pygame, random, time

pygame.init()

screen_width, screen_height = 1280, 720
real_width, real_height = 1333, 1055
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
circlelist = []
font = pygame.font.SysFont(None, 24)  
running = True

class Player:
    def __init__(self, x, y, size=13, speed = 5, value = 3, strikecount = 0, divisible_by_5_streak = 0):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.value = value
        self.strikecount = strikecount
        self.divisible_by_5_streak = divisible_by_5_streak

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx**2 + dy**2) ** 0.5

        if distance > self.speed:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        else:
            self.x = target_x
            self.y = target_y

        self.x = max(self.size, min(real_width - self.size, self.x))
        self.y = max(self.size, min(real_height - self.size, self.y))

    def grow(self, surface, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)

        pygame.draw.circle(surface, "green", (screen_x, screen_y), self.size)
        text = font.render(str(self.value), True, "black")
        text_rect = text.get_rect(center=(screen_x, screen_y))
        surface.blit(text, text_rect)

player = Player(real_width // 2, real_height // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera_x = player.x - screen_width // 2
    camera_y = player.y - screen_height // 2
    camera_x = max(0, min(real_width - screen_width, camera_x))
    camera_y = max(0, min(real_height - screen_height, camera_y))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    target_x = mouse_x + camera_x
    target_y = mouse_y + camera_y

    player.move(target_x, target_y)

    screen.fill("white")
    pygame.draw.rect(screen, "black", (-camera_x, -camera_y, real_width, real_height), 10)

    player.grow(screen, camera_x, camera_y)

    pygame.display.flip()
    clock.tick(60)

class Circle:
    def __init__(self, position, value, size, speed):
        self.position = position
        self.value = value
        self.size = size
        self.speed = speed
    def is_prime(self):
        if self.value <= 1:
            return False
        for i=2 to floor(sqrt(self.value)):
            if self.value % i==0, 
                return False
        return True

def collision_check(circlelist):
    for circle in circlelist:
        distance = 
        





pygame.quit()
