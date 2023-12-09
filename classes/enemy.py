import util
from util import *
import pygame
import time
import math

class Enemy():
    def __init__(self,surface,loc_x,loc_y,vx,vy,health):
        self.surface = surface
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.vx = vx
        self.vy = vy
        self.damage = 10
        self.speed = 1.9
        self.radius = 30
        self.last_attacked = time.time()
        self.attack_speed = 2 # per second
        self.health = health



    def render_self(self):
        pygame.draw.circle(self.surface, (255, 0, 0), (self.loc_x, self.loc_y), self.radius)

    def check_movement(self):
        self.loc_x += self.vx
        self.loc_y += self.vy
        self.vx = round(self.vx,2)
        self.vy = round(self.vy, 2)



    def move_to_player(self,player_loc_x,player_loc_y):

        x_direction,y_direction = util.normalize_vectors(self.loc_x,self.loc_y,player_loc_x,player_loc_y)
        self.vx = x_direction * self.speed
        self.vy = y_direction * self.speed

    def check_collision(self,player_loc_x,player_loc_y,player_radius):
        if math.sqrt((player_loc_x-self.loc_x)**2 + (player_loc_y-self.loc_y)**2) <= player_radius + self.radius:
            if time.time() - self.last_attacked > (1/self.attack_speed):
                self.last_attacked = time.time()
                return self.damage
            else:
                return 0
        else:
            return 0

    def check_death(self):
        if self.health <= 0:
            return True




