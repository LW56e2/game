import pygame
import math
import time
import util
from util import *
import random

class Player:
    def __init__(self,surface,loc_x,loc_y):


        self.loc_x = loc_x
        self.loc_y = loc_y
        self.surface = surface
        self.last_shot_time = time.time()
        self.chosen_class = None

        # will be changed during character selection

        self.speed = 2
        self.radius = 20
        self.bullet_speed = 10
        self.gun_length = 20
        self.gun_width = 10
        self.shots_per_second = 8
        self.health = 100
        self.points = 0
        self.bullet_radius = 10
        self.damage = 10

        self.bullet_is_penetrating = False
        self.bullet_is_cannonball = False
        self.bullet_is_bouncy = False



    def render_self(self):


        pygame.draw.circle(self.surface,(0,255,255),(self.loc_x,self.loc_y),self.radius)
        pygame.draw.circle(self.surface,(204, 102, 255), (self.loc_x, self.loc_y), self.radius/1.5)

    def check_movement(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.loc_y > 0:
                self.loc_y -= self.speed
        if keys[pygame.K_s]:
            if self.loc_y < 720:
                self.loc_y += self.speed
        if keys[pygame.K_a]:
            if self.loc_x > 0:
                self.loc_x -= self.speed
        if keys[pygame.K_d]:
            if self.loc_x < 1280:
                self.loc_x += self.speed




    def check_shoot(self,surface):



        target_x,target_y = pygame.mouse.get_pos()

        normalized_vector = util.normalize_vectors(self.loc_x,self.loc_y,target_x,target_y)
        if normalized_vector:
            x_direction,y_direction = normalized_vector
        else:
            return None
        vx = x_direction * self.bullet_speed
        vy = y_direction * self.bullet_speed

        gun_base_x = self.loc_x + x_direction * self.radius/2
        gun_base_y = self.loc_y + y_direction * self.radius/2


        gunpoint_x = self.loc_x + x_direction * (self.gun_length + self.radius)
        gunpoint_y = self.loc_y + y_direction * (self.gun_length + self.radius)


        half_width = self.gun_width / 2

        # Perpendicular direction
        perp_x = -y_direction
        perp_y = x_direction

        # Calculate corners
        corner1_x = gun_base_x + perp_x * half_width
        corner1_y = gun_base_y + perp_y * half_width

        corner2_x = gun_base_x - perp_x * half_width
        corner2_y = gun_base_y - perp_y * half_width

        corner3_x = gunpoint_x - perp_x * half_width
        corner3_y = gunpoint_y - perp_y * half_width

        corner4_x = gunpoint_x + perp_x * half_width
        corner4_y = gunpoint_y + perp_y * half_width

        pygame.draw.polygon(surface,(255,0,255),((corner1_x,corner1_y),(corner2_x,corner2_y),(corner3_x,corner3_y),(corner4_x,corner4_y)))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if time.time() - self.last_shot_time > (1/self.shots_per_second):
                from classes import Generalized_Bullet

                if self.chosen_class == 'Tank' or self.chosen_class == 'Scout' or self.chosen_class == "Sniper" or self.chosen_class == "Cannoneer" \
                        or self.chosen_class == "Archer":
                    possible_shot = Generalized_Bullet(self.surface, gunpoint_x, gunpoint_y, vx, vy, self.bullet_radius, self.damage,
                                                       is_cannonball=self.bullet_is_cannonball, is_penetrating=self.bullet_is_penetrating, is_bouncy=self.bullet_is_bouncy)


                    shot = possible_shot
                    self.last_shot_time = time.time()
                    return [shot] # a list of shots with only one shot


                if self.chosen_class == 'Shotgunner':
                    shot_list = []
                    for i in range (1,20):
                        x_modifier = random.uniform(-2, 2)
                        y_modifier = random.uniform(-2, 2)
                        shot_list.append(Generalized_Bullet(self.surface, gunpoint_x, gunpoint_y, vx + x_modifier, vy + y_modifier, self.bullet_radius, self.damage,
                                                       is_cannonball=self.bullet_is_cannonball, is_penetrating=self.bullet_is_penetrating))

                    self.last_shot_time = time.time()
                    return shot_list

                if self.chosen_class == 'Exploder':
                    shot_list = []
                    all_vectors = create_circular_normalized_vectors(30)
                    for vector in all_vectors:
                        if vector:
                            shot_list.append(Generalized_Bullet(self.surface, gunpoint_x, gunpoint_y, vector[0] * self.bullet_speed, vector[1] * self.bullet_speed,
                                                                self.bullet_radius, self.damage))

                    self.last_shot_time = time.time()
                    return shot_list

                if self.chosen_class == 'Sprayer':

                    x_modifier = random.uniform(-2, 2)
                    y_modifier = random.uniform(-2, 2)
                    shot = Generalized_Bullet(self.surface, gunpoint_x, gunpoint_y, vx + x_modifier, vy + y_modifier, self.bullet_radius, self.damage,
                                               is_cannonball=self.bullet_is_cannonball, is_penetrating=self.bullet_is_penetrating)

                    self.last_shot_time = time.time()
                    return [shot]

                pass

    def check_death(self):
        if self.health <= 0:
            return True



