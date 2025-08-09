from pygame import *

class GameSprite(sprite.Sprite):
    def _init_(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite._init_(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def _init_(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite._init_(self, player_image,player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    def update(self):
        if hero1.rect.x <= win_width-80 and hero1.x_speed > 0 or hero1.rect.x >= 0 and hero1.x_speed < 0:
            self.rect.x += self.x_speed
            
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                
        if hero1.rect.y <= win_height-80 and hero1.y_speed > 0 or hero1.rect.y >= 0 and hero1.y_speed < 0:
            self.rect.y += self.y_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) 

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect >= win_width - 85:
            self.side ="left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

win_width = 700
win_height = 500
display.set_caption('Maze game')
window = display.set_mode((win_width, win_height))
back = (200, 150, 180)

#creating a group for the walls
barriers = sprite.Group()

monsters = sprite.Group()

w1 = GameSprite('Wall.png',win_width / 2 - win_width / 3, win_height/2, 300, 50)
w2 = GameSprite('Wall.png', 370, 100, 50, 400)

#adding walls to the group
barriers.add(w1)
barriers.add(w2)

hero1 = Player('THE JOJ.png', 5, win_height - 80, 80, 80, 0, 0)

monster1 = Enemy('sf.png', win_width - 80, 180, 80, 80, 5)
monster2 = Enemy('dsfdf.png', win_width - 80, 230, 80, 80, 5)

monsters.add(w1)
monsters.add(w2)

final_sprite = GameSprite('dadada.png', win_width - 85, win_height - 100, 80, 80)

finish = False

run = True
while run:
    time.delay(50)
    window.fill(back)

    for e in event.get():
        if e.type == QUIT:
            run = False
            
        elif e.type == KEYDOWN:
            if e.key == K_d:
                hero1.x_speed = 10
            elif e.key == K_a:
                hero1.x_speed = -1
            elif e.key == K_w:
                hero1.y_speed = -1
            elif e.key == K_s:
                hero1.y_speed = 10
        
        elif e.type == KEYUP:
            if e.key == K_d:
                hero1.x_speed = 0
            elif e.key == K_a:
                hero1.x_speed = 0
            elif e.key == K_w:
                hero1.y_speed = 0
            elif e.key == K_s:
                hero1.y_speed = 0

    if not finish:
        window.fill(back)
        barriers.draw(window)

        monsters.update()
        monsters.draw(window)

        final_sprite.reset()
        hero1.reset()
        hero1.update()

    if sprite.spritecollide(hero1, monsters, False):
       finish = True
       #calculate the ratio
       img = image.load('GAME OVER.jpg')
       d = img.get_width() // img.get_height()
       window.fill((255, 255, 255))
       window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


    if sprite.collide_rect(hero1, final_sprite):
       finish = True
       img = image.load('Thumb.jpeg')
       window.fill((255, 255, 255))
       window.blit(transform.scale(img, (win_width, win_height)), (0, 0))



    # w1.reset()
    # w2.reset()
    

    display.update()