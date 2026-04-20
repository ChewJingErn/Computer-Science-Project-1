import math, pygame, random, time
pygame.init()

screen_width, screen_height = 1280, 720
real_width, real_height = 1333, 1055
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)  

def get_primes(limit): #to display prime numbers on menu and gameover screen
    primes = []
    for n in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)
    return primes
prime_list = get_primes(150)

def draw_prime_list(surface): #displaying prime numbers
    title = font.render("List of prime numbers:", True, "black")
    surface.blit(title, (20, 20))
    y = 50
    for p in prime_list:
        text = font.render(str(p), True, "black")
        surface.blit(text, (20, y))
        y += 18

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 13
        self.speed = 5
        self.value = 3
        self.strikecount = 0
        self.divisible_by_5_streak = 0
        self.start_time = pygame.time.get_ticks()

    def move(self, target_x, target_y): #how player circle moves
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance < 1:
            return 
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        
        self.x = max(self.size, min(real_width - self.size, self.x))
        self.y = max(self.size, min(real_height - self.size, self.y))

    def grow(self, amount): #how player circle grows
        max_size = 65
        self.value += amount
        new_size = 10 + self.value * 0.25
        self.size = min(max_size, new_size)
        
    def draw(self, surface, camera_x, camera_y): #player circle 
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        pygame.draw.circle(surface, "green", (screen_x, screen_y), int(self.size))
        text = font.render(str(self.value), True, "black")
        surface.blit(text, text.get_rect(center=(screen_x, screen_y)))

class Circle:
    def __init__(self, player_value, forced_value=None):
        self.x = random.randint(0, real_width)
        self.y = random.randint(0, real_height)
        
        if player_value <= 200: #Setting a cap
            min_value = max(1, int(player_value * 0.6))
            max_value = min(200, player_value + 10)
        else:
            min_value = 100
            max_value = 200

        if forced_value is not None:
            self.value = forced_value
        else:
            self.value = random.randint(min_value, max_value)

        max_size = 60
        self.size = min(max_size, 10 + math.sqrt(self.value) * 4)
        speed = 2
        
        angle = random.random() * math.pi * 2
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
    def move(self): #circle movement
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > real_width:
            self.dx *= -1
        if self.y < 0 or self.y > real_height:
            self.dy *= -1

    def spawn(self, surface, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        colour = "darkred" if self.is_prime() and self.value > 150 else "red"

        pygame.draw.circle(surface, colour, (screen_x, screen_y), int(self.size))
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
    def __init__(self):
        self.player = None
        self.circlelist = []
        self.screendisplay = "menu"
        self.time = 0
        self.clicked = False
        self.play_button = pygame.Rect(screen_width//2 - 100, 500, 200, 60)
        self.win_score = 1505
        self.rules = {
            1: "1. Only eat smaller numbers to grow.",
            2: "2. Eating a prime number will result in a strike.",
            3: "3. Obtaining 3 strikes will result in a lose.",
            4: "4. Eating a number that is a multiple of 5, 3 times in a row, will give you bonus growth!",
            5: "5. Obtain a win score of up to 1505!",
        }

    def start_game(self):
        self.player = Player(real_width // 2, real_height // 2)
        self.player.start_time = pygame.time.get_ticks()
        self.circlelist = []
        edible_value = self.generate_edible_value()
        self.circlelist.append(Circle(self.player.value, forced_value=edible_value))
        for i in range(7):
            if random.random() < 0.25:
                self.circlelist.append(Circle(self.player.value, forced_value=self.generate_edible_value()))
            else:
                self.circlelist.append(Circle(self.player.value))
        self.screendisplay = "playing"

    def game_win(self):
        if self.player.strikecount >= 1:
            self.win_score = 995
        else:
            self.win_score = 1505
        if self.player.value >= self.win_score:
            self.final_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
            self.screendisplay = "win"

    def game_lose(self):
        if self.player.strikecount >= 3:
            self.screendisplay = "lost"
            self.final_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
        
    def collision_check(self):
        for circle in self.circlelist[:]:
            distance = math.hypot(self.player.x - circle.x, self.player.y - circle.y)
            
            if distance < self.player.size + circle.size:
                if circle.value > self.player.value:
                    self.final_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
                    self.screendisplay = "lost"
                    return

                if circle.is_prime():
                    self.player.strikecount += 1
                self.player.grow(circle.value)
                    
                if circle.value % 5 == 0:
                    self.player.divisible_by_5_streak += 1
                    if self.player.divisible_by_5_streak == 3:
                        bonus = int(self.player.value * 0.05)
                        self.player.grow(bonus)
                        self.player.divisible_by_5_streak = 0
                else:
                    self.player.divisible_by_5_streak = 0
                    
                self.circlelist.remove(circle)
                if random.random() < 0.3:
                    new_value = self.generate_edible_value()
                    self.circlelist.append(Circle(self.player.value, forced_value=new_value))
                else:
                    self.circlelist.append(Circle(self.player.value))
                break

    def gameplay(self):
        screen.fill("white")
        camera_x = self.player.x - screen_width // 2
        camera_y = self.player.y - screen_height // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player.move(mouse_x + camera_x, mouse_y + camera_y)

        for circle in self.circlelist:
            circle.move()
        self.collision_check()
        self.ensure_safe_circle()
        self.game_win()
        self.game_lose()

        for circle in self.circlelist:
            circle.spawn(screen, camera_x, camera_y)
        self.player.draw(screen, camera_x, camera_y)
        elapsed_ms = pygame.time.get_ticks() - self.player.start_time
        elapsed_sec = elapsed_ms / 1000

        timedisplay = font.render(f"Time: {elapsed_sec:.2f} s", True, "black")
        screen.blit(timedisplay, (screen_width - 180, 20))
        strikedisplay = font.render(f"Strikes: {self.player.strikecount}/3", True, "black")
        screen.blit(strikedisplay, (screen_width - 150, 50))
            
    def menu_display(self):
        screen.fill("white")
        draw_prime_list(screen)
        title_font = pygame.font.SysFont(None, 80)
        title = title_font.render("ODDBALL", True, "black")
        screen.blit(title, title.get_rect(center=(screen_width//2, 100)))

        for i in range(1, 6):
            text = font.render(self.rules[i], True, "black")
            screen.blit(text, text.get_rect(center=(screen_width//2, 260 + (i-1)*35)))

        pygame.draw.rect(screen, "green", self.play_button) 
        play_text = font.render("PLAY", True, "white") 
        screen.blit(play_text, play_text.get_rect(center=self.play_button.center))

        if self.clicked and self.play_button.collidepoint(pygame.mouse.get_pos()):
            self.start_game()

    def gameover_screen(self):
        screen.fill("white")
        draw_prime_list(screen)
        title = pygame.font.SysFont(None, 70).render("YOU LOSE!", True, "red")
        screen.blit(title, title.get_rect(center=(screen_width//2, 120)))
        timedisplay = font.render(f"Time: {self.final_time:.2f} s", True, "black")
        screen.blit(timedisplay, timedisplay.get_rect(center=(screen_width//2, 200)))
            
        score_text = font.render(f"Score: {int(self.player.value)}", True, "black")
        screen.blit(score_text, score_text.get_rect(center=(screen_width//2, 180)))

        strike_text = font.render(f"Strikes: {self.player.strikecount}/3", True, "red")
        screen.blit(strike_text, strike_text.get_rect(center=(screen_width//2, 220)))

        for i in range(1, 6):
            text = font.render(self.rules[i], True, "black")
            screen.blit(text, text.get_rect(center=(screen_width//2, 260 + (i-1)*35)))

        retry = retry = pygame.Rect(screen_width//2 - 50, 650, 100, 50)
        pygame.draw.rect(screen, "green", retry)
        retry_text = font.render("Retry", True, "white")

        screen.blit(retry_text, retry_text.get_rect(center=retry.center))

        if self.clicked:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if retry.collidepoint(mouse_x, mouse_y):
                self.start_game()

    def win_screen(self):
        screen.fill("white")
        text = pygame.font.SysFont(None, 80).render("YOU WON!", True, "green")
        screen.blit(text, text.get_rect(center=(screen_width//2, 100)))
        
        menu_button = pygame.Rect(screen_width//2 - 100, 500, 200, 60)
        pygame.draw.rect(screen, "blue", menu_button)

        timedisplay = font.render(f"Time: {self.final_time:.2f} s", True, "black")
        screen.blit(timedisplay, timedisplay.get_rect(center=(screen_width//2, 200)))
        
        score_text = font.render(f"Score: {int(self.win_score)}",True,"black")
        screen.blit(score_text, score_text.get_rect(center=(screen_width//2, 180)))

        strike_text = font.render(f"Strikes: {self.player.strikecount}/3", True, "orange" if self.player.strikecount > 0 else "green")
        screen.blit(strike_text, strike_text.get_rect(center=(screen_width//2, 220)))
        
        menu_button = pygame.Rect(screen_width//2 - 100, 500, 200, 60)
        pygame.draw.rect(screen, "blue", menu_button)

        text = font.render("Menu", True, "white")
        screen.blit(text, text.get_rect(center=menu_button.center))

        if self.win_score == 995:
            hint_score = font.render("Try getting 0 strikes next round!", True, "black")
            screen.blit(hint_score, hint_score.get_rect(center=(screen_width//2, 260)))
  
        if self.clicked:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if menu_button.collidepoint(mouse_x, mouse_y):
                self.start_game()
                self.screendisplay = "menu"

    def screen(self):
        if self.screendisplay == "menu":
            self.menu_display()
        elif self.screendisplay == "playing":
            self.gameplay()
        elif self.screendisplay == "lost":
            self.gameover_screen()
        elif self.screendisplay == "win":
            self.win_screen()
    
    def start(self):
        self.screendisplay = "menu"

    def generate_edible_value(self):
        while True:
            value = max(1, self.player.value - random.randint(1, 5))
            value = min(200, value)

            if self.player.value > 200:
                value = max(100, value)

            if value > 1:
                prime = True
                for i in range(2, int(math.sqrt(value)) + 1):
                    if value % i == 0:
                        prime = False
                        break
                if not prime:
                    return value
            else:
                return value
    def ensure_safe_circle(self):
        for circle in self.circlelist:
            if circle.value < self.player.value and not circle.is_prime():
                return
        safe_value = self.generate_edible_value()
        self.circlelist.append(Circle(self.player.value, forced_value=safe_value))

game = Game()
running = True

while running:
    game.clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.clicked = True            
            
    game.screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
