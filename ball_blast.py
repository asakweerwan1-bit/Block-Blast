from typing import Any

import pygame, math, random

pygame.init()


class Ball(pygame.sprite.Sprite):
    
    
    def __init__(self,posx:int,posy:int,color=(0,0,0),xsize=10,ysize=10,speed_factorx=2, speed_factory=2) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface((xsize,ysize))
        self.color = color
        self.image.fill(self.color)
        if len(Ball_group) == 1:
            self.ball_speed = [random.randint(1,2) , random.randint(1,2)]
        else:
            self.ball_speed = [random.randint(2,3) , random.randint(2,3)]
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)
  
        self.start_direction = random.randint(0, 1)
        if self.start_direction == 0:
            self.ball_speed[0] *= -1
        
    def update(self,player,rand=False):

        global RECT_WIDTH
        
        self.rect.x += self.ball_speed[0]
        self.rect.y +=self.ball_speed[1]
        
        if self.rect.x <= 0 :
            self.ball_speed[0] = -self.ball_speed[0]
            self.ball_speed[0] += 0.25

        elif  ( self.rect.x >= WIN_WIDTH ):
             self.ball_speed[0] = -self.ball_speed[0]
             self.rect.right=WIN_WIDTH-1
               
        elif (self.rect.y <= 0):
             self.ball_speed[1] = self.ball_speed[1]*-1
             self.ball_speed[0] += 1
        elif self.rect.y >= WIN_HEIGHT:
             self.kill()
             
                
        elif self.rect.colliderect(player):
            self.ball_speed[1] = self.ball_speed[1]*-1

            if self.ball_speed[0] > 0:
                self.ball_speed[0] += 0.0625
                self.ball_speed[1] += 0.0625
            elif self.ball_speed[0] < 0:
                self.ball_speed[0] -= 1
                self.ball_speed[1] += 0.0625

            self.rect.bottom=player.top
            if self.color == 'orange':
                 RECT_WIDTH +=10
                 self.kill()
          
            if self.ball_speed[0] < 0 and self.rect.left >= player.right:
                            self.ball_speed[0]*=-1


        spritedict = pygame.sprite.groupcollide(Ball_group,group,False,True)
        
        if spritedict:

            if self.rect.x > 0 or ( self.rect.x > WIN_WIDTH ):
                self.ball_speed[1] = self.ball_speed[1]*-1
        
           
            if self.color == (100,200,100):

                self.ball_speed[0]+=0.0625
    
        for k, v in spritedict.items():
            for sprite in v:
                
                if sprite.color == 'red':
                    if len(Ball_group) > 1:
                        for i in range(0,math.ceil(len(Ball_group)/2)):
                            
                            Ball_group.remove(Ball_group.sprites()[-i])
                            

                elif sprite.color == 'orange':
                    Ball_group.add(Ball(self.rect.topleft[0],self.rect.topleft[1],color='orange'))
                    Ball_group.add(Ball(self.rect.topleft[0],self.rect.topleft[1]))


                elif sprite.color == 'purple':
                    Ball_group.add(Ball(self.rect.topleft[0],self.rect.topleft[1],color=(100,200,100),xsize=7, ysize=7,
                                        speed_factorx=random.randint(3,6),
                                        speed_factory=random.randint(3,6)))

                


class Square(pygame.sprite.Sprite):
    def __init__(self,col:str|tuple,x:int, y:int, pos_x:int, pos_y:int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface((x,y))
        self.image.fill(col)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)


class TheTiles:
    def __init__(self:TheTiles, screen:pygame.Surface) -> None:
        self.screen = screen
        self.destructibles =pygame.sprite.Group()
        self.grid_size=20
    def _init_group_(self):
        return self.destructibles

    def draw_grid(self,numberLines:int,grid_size:int, y_spacing:int=0):
        self.grid_size = grid_size
        if y_spacing == 0:
            y_spacing=grid_size
        for i in range(numberLines):            
    
            pygame.draw.line(self.screen, (255,255,255),(0,i*grid_size),(WIN_WIDTH, i*grid_size))
            pygame.draw.line(self.screen, (255,255,255),(i*y_spacing,0),(i*y_spacing,WIN_HEIGHT))  

        return (grid_size, y_spacing)
    
    def add_squares(self, x, y, posx, posy, group, color=(0,0,0)):
        
        square = Square(color,x, y,posx,posy)
        setattr(square,'color',color)

        group.add(square)
  

    def group(self, numberLines=13, grid_size=20,y_spacing=50, number_per_Line=10):

        y_spacing=30
        grid_size=10
        
        if y_spacing == 0:
            y_spacing=grid_size

        for line in range(numberLines):
            for i in range(number_per_Line):
                num=random.randint(1,10)
                red = random.randint(0,75)
                color=(0,0,0)
                if num == 10:
                     color='orange'
                elif num == 1:
                     color='purple'
                if red==75:
                     color='red'
                
                self.add_squares(y_spacing,grid_size,i*y_spacing,line*grid_size,self.destructibles,color=color)
        return self.destructibles



WIN_HEIGHT = 500
WIN_WIDTH = 500
WHITE = (255,255,255)
BLACK = (0,0,0)
 
RECT_WIDTH = 50

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('Ball Blast 2026© Bambouillinous')

Ball_group = pygame.sprite.Group()

Tiles = TheTiles(screen)
group=Tiles.group(numberLines=25,number_per_Line=17)
clock = pygame.Clock()
x1 = WIN_WIDTH/2
y1 = 390

ball_x = 200
ball_y = 260


player_x = 4


running = False

ball_index =0





number_of_balls = 2

for i in range(number_of_balls):
     Ball_group.add(Ball(ball_x,ball_y))
   

while not running:
    player_x += 0.00125
    
    screen.fill(WHITE)

    #
    
    player = pygame.draw.rect(screen,BLACK,(x1,y1,RECT_WIDTH,8))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=True

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        x1 = max(0,x1-player_x)
    elif key[pygame.K_RIGHT]:
            x1 = min(WIN_WIDTH-RECT_WIDTH,x1+player_x)

    

    ball_collided = pygame.sprite.groupcollide(Ball_group,group,False,True)

    Ball_group.update(player)
    Ball_group.draw(screen)    
    group.draw(screen)
    group.update()

    

    #Tiles.draw_grid(30,20,50)
    Tiles.draw_grid(30,10,30)

    pygame.display.flip()
    clock.tick(1000/16)


