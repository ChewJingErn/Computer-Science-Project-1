import math, pygame, random, time

pygame.init()

screen_width, screen_height = 1280, 720
real_width, real_height = 1333, 1055
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)  
running = True

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 13
        self.speed = 5
        self.value = 3
        self.strikecount = 0
        self.divisible_by_5_streak = 0

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance < 1:
            return 
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        
        self.x = max(self.size, min(real_width - self.size, self.x))
        self.y = max(self.size, min(real_height - self.size, self.y))

    def grow(self, amount):
        self.value += amount
        self.size = 10 + self.value * 0.3
    def draw(self, surface, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        pygame.draw.circle(surface, "green", (screen_x, screen_y), int(self.size))
        text = font.render(str(self.value), True, "black")
        surface.blit(text, text.get_rect(center=(screen_x, screen_y)))

class Circle:
    def __init__(self, player_value=None, forced_value=None):
        self.x = random.randint(0, real_width)
        self.y = random.randint(0, real_height)
        if forced_value is not None:
            self.value = forced_value
        else:
            self.value = random.randint(1, player_value + 10)
        self.size = 10 + math.sqrt(self.value) * 4
        
        speed = 2
        angle = random.random() * math.pi * 2
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > real_width:
            self.dx *= -1
        if self.y < 0 or self.y > real_height:
            self.dy *= -1

    def spawn(self, surface, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)

        pygame.draw.circle(surface, "red", (screen_x, screen_y), int(self.size))
        text = font.render(str(self.value), True, "white")
        surface.blit(text, text.get_rect(center=(screen_x, screen_y)))
                           
    def is_prime(self):
        if self.value <= 1:
            return False
        for i in range(2, int(math.sqrt(self.value)) + 1):
            if self.value % i == 0:
                return False
        return True
        
class Game:
    def __init__(self, player, circlelist, strikecount, screendisplay, time, winscore, mapwidth, mapheight):
        self.player = player
        self.circlelist = circlelist
        self.strikecount = strikecount
        self.screendisplay = screendisplay
        self.time = time
        self.winscore = winscore
        self.mapwidth = mapwidth
        self.mapheight = mapheight
    def start(self):
        self.screendisplay = "menu"
    def collision_check(circlelist):
            if distance < player.size + circle.size:
                if circle.value > player.value:
                    running = Flase
                else:
                    player.grow(circle.value)
                    if circle.is_prime():
                        player.strikecount += 1
                circlelist.remove(circle)
                circlelist.append(Circle(player.value))


player = Player(real_width // 2, real_height // 2)
circlelist = [Circle(player.value) for _ in range(8)]
running = True

def edible_circle():
    for circle in circlelist:
        if circle.value < player.value:
            return 
    new_circle = max(1, player.value - random.randint(1, 5))

    while True:
        is_prime = True
        if new_circle <= 1:
            is_prime = False
        else:
            for i in range(2, int(math.sqrt(new_circle)) + 1):
                if new_circle % i == 0:
                    is_prime = False
                    break
        if not is_prime:
            break
        new_circle = max(1, player.value - random.randint(1, 5))
    circlelist.append(Circle(forced_value=new_circle))

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
    for circle in circlelist:
        circle.move()
    for circle in circlelist[:]:
        distance = math.hypot(player.x - circle.x, player.y - circle.y)
        if distance < player.size + circle.size:
            if circle.value > player.value:
                running = False
            else: 
                player.grow(circle.value)
                if circle.is_prime():
                    player.strikecount += 1

                circlelist.remove(circle)
                circlelist.append(Circle(player.value))

    if player.strikecount >= 3
        running = False
    screen.fill("white")
    player.draw(screen, camera_x, camera_y)
    for circle in circlelist:
        circle.spawn(screen, camera_x, camera_y)
        
    strike_text = font.render(f"Strike Count: {player.strikecount}/3", True, "black")
    screen.blit(strike_text, (screen_width - strike_text.get_width() - 20, 20))
    edible_circle()
    pygame.display.flip()
    clock.tick(60)





pygame.quit()
