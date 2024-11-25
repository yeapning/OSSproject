import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        pass



class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        # ============================================ ㄴ
        # TODO: Implement an event when the ball hits a block
        pass
        index = pygame.Rect.collidelist(self.rect,[Block.rect for Block in blocks])
        if(index >= 0):
            blocks[index].collide()
            self.Change_direct(blocks[index])


    def Change_direct(self, obj: Basic):
        rect_sum_x = self.rect.width + obj.rect.width
        rect_sum_y = self.rect.height + obj.rect.height

        gap_x = self.rect.centerx - obj.rect.centerx
        gap_y = self.rect.centery - obj.rect.centery
        

        overX = gap_x - (2*(gap_x > 0)-1) * rect_sum_x
        overY = gap_y - (2*(gap_y > 0)-1) * rect_sum_y
        #x 양수면 왼쪽에서 부딪힌거 y 양수면 위에서 부딪힌거
        #과잉: 두개가 맞닿았을때, 겹쳐진 부분의 길이.
        if(abs(overX) >= abs(overY)):#수평 충돌체와 충돌
            if(self.rect.centery > obj.rect.centery): #아래로 튐
                self.down_bound()
                print("하",self.dir)
            else:                         #위로 튐
                self.up_bound()
                print("상",self.dir)
        else:#수직 충돌체와 충돌
            if(self.rect.centerx < obj.rect.centerx): #오른쪽으로 튐
                self.left_bound()
                print("좌",self.dir)
            else:                         #왼쪽로 튐
                self.right_bound()
                print("우",self.dir)


    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.Change_direct(paddle)

    def hit_wall(self): 
        if (self.rect.centerx + self.rect.width > config.display_dimension[0] or self.rect.centerx < 0):
            self.dir = 360 - (self.dir - 180)
            self.dir = self.dir%360
        if (self.rect.centery < 0):
            self.dir = 360 - self.dir

    def up_bound(self): 
        if 180 <= self.dir and self.dir < 360: #위에서 아래로
            self.dir = 360 - self.dir
    
    def down_bound(self): 
        if 0 <= self.dir and self.dir < 180: #위에서 아래로
            self.dir = 360 - self.dir
        self.dir = self.dir%360

    def left_bound(self):
        if 270 <= self.dir and self.dir < 360: #위에서 아래로
            self.dir = 360 - (self.dir - 180)
        elif 0 <= self.dir and self.dir < 90:
            self.dir = 180 - self.dir
        self.dir = self.dir%360

    def right_bound(self):
        if 90 <= self.dir and self.dir < 270: #위에서 아래로
            self.dir = 360 - (self.dir - 180)
        self.dir = self.dir%360

    def alive(self):
       return self.rect.centery < config.display_dimension[1]