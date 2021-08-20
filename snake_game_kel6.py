import pygame
from pygame.locals import *
import time
import random

SIZE = 20

#Kelas untuk Apple, mengatur tampilan dan posisi apel
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("assets/apple.png").convert_alpha()
        self.x = random.randint(1,22)*SIZE
        self.y = random.randint(1,22)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,22)*SIZE
        self.y = random.randint(1,22)*SIZE
        
#Kelas untuk menu Start, menampilkan layar start
class Start :
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.bg_start = pygame.image.load("assets/bg_starts.png").convert_alpha()
        self.x = 0
        self.y = 0

    def drawstart(self):
        self.parent_screen.blit(self.bg_start, (self.x, self.y))
        pygame.display.flip()
        
#Kelas untuk Balok rintangan, mengatur tampilan dan posisi balok
class Wall:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.walls = pygame.image.load("assets/wallblock.png").convert_alpha()
        self.xw = random.randint(1,22)*SIZE
        self.yw = random.randint(1,22)*SIZE
        
    def draw(self):
        self.parent_screen.blit(self.walls, (self.xw, self.yw))
        pygame.display.flip()

    def move(self):
        self.xw = random.randint(1,22)*SIZE
        self.yw = random.randint(1,22)*SIZE

#Kelas untuk mengatur Ular
class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.bg_surface = pygame.image.load('assets/background_img.png').convert()         
        self.blockhead = pygame.image.load("assets/snake_heads.png").convert_alpha()
        self.block = pygame.image.load("assets/snake_body.png").convert_alpha()
        self.direction = 'RIGHT'

        self.length = 1
        self.x = [20]
        self.y = [20]
    
    #Fungsi untuk mengatur variabel yang menunjukkan status pergerakan ular
    def move_left(self):
        self.direction = 'LEFT'

    def move_right(self):
        self.direction = 'RIGHT'

    def move_up(self):
        self.direction = 'UP'

    def move_down(self):
        self.direction = 'DOWN'
    
    #Fungsi untuk mengatur rotasi dari kepala ular agar sesuai dengan arah bergeraknya
    def rotate90(self):
        self.blockhead = pygame.transform.rotate(self.blockhead, 90)
        self.block = pygame.transform.rotate(self.block, 90)

    def rotate270(self):
        self.blockhead = pygame.transform.rotate(self.blockhead, 270)
        self.block = pygame.transform.rotate(self.block, 270)
    
    #Fungsi untuk pergerakan ular (ular berjalan ke arah tertentu)
    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'LEFT':
            self.x[0] -= SIZE
        if self.direction == 'RIGHT':
            self.x[0] += SIZE
        if self.direction == 'UP':
            self.y[0] -= SIZE
        if self.direction == 'DOWN':
            self.y[0] += SIZE

        self.draw()
    
    #Fungsi untuk mengatur tampilan ular saat ular bergerak
    def draw(self):  
        self.parent_screen.blit(self.bg_surface, (0,0))                                             
                                        
        for i in range(self.length):      
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        self.parent_screen.blit(self.blockhead, (self.x[0], self.y[0]))     
        pygame.display.flip()
    
    #Fungsi untuk menambah panjang ular
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

#Kelas untuk menjalankan permainan secara keseluruhan
class Game:    
    def __init__(self):
        pygame.init()        
        pygame.display.set_caption("Snake Game by Group F WiT")               
        self.surface = pygame.display.set_mode((720, 480))                    
        self.snake = Snake(self.surface)       
        self.apple = Apple(self.surface)  
        self.wall = Wall(self.surface)
        self.starts = Start(self.surface)   
        self.snake.draw() 
        self.starts.drawstart()
        pygame.mixer.init()       
        self.play_bg_music()
    
    #Fungsi untuk memainkan background music
    def play_bg_music(self):
        pygame.mixer.music.load("assets/bgmusic.mp3")  
        pygame.mixer.music.play(-1,0)
    
    #Fungsi untuk mengatur sound effect yang dimainkan saat ular makan atau menabrak
    def play_sound(self,sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("assets/bghit.mp3")
        elif sound_name == "munch":
            sound = pygame.mixer.Sound("assets/bgmunch.mp3")
        pygame.mixer.Sound.play(sound)
    
    #Fungsi untuk reset
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
    
    #Fungsi untuk mengatur apabila ular menabrak objek tertentu
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    #Fungsi untuk memulai permainan, dimana pada fungsi ini memanggil fungsi-fungsi dari kelas lain
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.wall.draw()      
        self.display_score()
        pygame.display.flip()

        # Ular makan apel
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("munch")
            self.snake.increase_length()
            self.apple.move()
            self.wall.move()

        # Ular memakan balok/menabrak balok
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.wall.xw, self.wall.yw):
            self.play_sound("crash")
            raise "Collision Occured"

        # Ular memakan badannya sendiri
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("munch")
                raise "Collision Occured"

        # Ular menabrak tepian layar permainan
        if self.snake.x[0] >= 720 or self.snake.x[0] < 0 or self.snake.y[0] >= 480 or self.snake.y[0] < 0:
            self.play_sound("crash")
            raise "Collision Occured"
    
    #Fungsi untuk menampilkan skor pada pinggiran/pojok layar secara real time
    def display_score(self):
        game_font = pygame.font.Font('assets/Pixellari.ttf',30)
        score = game_font.render(f"Score: {self.snake.length-1}",True,(255,255,255))
        self.surface.blit(score,(10,10))
    
    #Fungsi untuk menampilkan skor saat game over, memberhentikan musik saat game over
    def show_game_over(self):
        self.bg_gameover = pygame.image.load('assets/bg_gameover.png').convert()
        self.surface.blit(self.bg_gameover, (0,0))
        font = pygame.font.Font('assets/Pixellari.ttf',30)
        line1 = font.render(f"Game Over!! Your score is {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(line1, (170, 200))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (35, 230))
        pygame.mixer.music.stop()
        pygame.display.flip()        
    
    #Fungsi untuk mengatur pergerakan ular saat permainan
    def run(self):                         
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:                      
                    running = True
                    pause = False                        
                    while running:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                    
                                if event.key == K_ESCAPE:
                                    exit()
                                    
                                if event.key == K_RETURN:
                                    pygame.mixer.music.play(-1,0)
                                    pause = False
                                
                                #Pergerakan ular diatur oleh input panah di keyboard
                                if self.snake.direction == 'RIGHT':
                                    if event.key == K_RIGHT:
                                        self.snake.move_right()
                                    if event.key == K_UP:
                                        self.snake.rotate90()
                                        self.snake.move_up()
                                    if event.key == K_DOWN:
                                        self.snake.rotate270()
                                        self.snake.move_down()    

                                elif self.snake.direction == 'LEFT':
                                    if event.key == K_LEFT:
                                        self.snake.move_left()
                                    if event.key == K_UP:
                                        self.snake.rotate270()
                                        self.snake.move_up()
                                    if event.key == K_DOWN:
                                        self.snake.rotate90()
                                        self.snake.move_down()

                                elif self.snake.direction == 'UP':
                                    if event.key == K_LEFT:
                                        self.snake.rotate90()
                                        self.snake.move_left()
                                    if event.key == K_RIGHT:
                                        self.snake.rotate270()
                                        self.snake.move_right()
                                    if event.key == K_UP:
                                        self.snake.move_up()
                                            
                                elif self.snake.direction == 'DOWN':
                                    if event.key == K_LEFT:
                                        self.snake.rotate270()
                                        self.snake.move_left()
                                    if event.key == K_RIGHT:
                                        self.snake.rotate90()
                                        self.snake.move_right()
                                    if event.key == K_DOWN:
                                        self.snake.move_down()

                            elif event.type == QUIT:
                                exit()

                        #Exception untuk game over
                        try:
                            if not pause:
                                self.play()

                        except Exception as e:
                            self.show_game_over()
                            pause = True
                            self.reset()

                        #Fungsi untuk mengatur pergerakan ular (diatur oleh clock) dimana pegerakan ular semakin cepat apabila mencapai skor tertentu
                        if self.snake.length-1 <= 7:
                            time.sleep(.2)
                        elif self.snake.length-1 > 7 and self.snake.length-1 <= 15:
                            time.sleep(.15)
                        elif self.snake.length-1 > 15 and self.snake.length-1 <= 30:
                            time.sleep(.1)
                        elif self.snake.length-1 > 30 and self.snake.length-1 <= 50:
                            time.sleep(.07)
                        else:
                            time.sleep(.05)
                            
                elif event.type == QUIT:
                    exit()
           
if __name__ == '__main__':   
    game = Game()
    game.run()
