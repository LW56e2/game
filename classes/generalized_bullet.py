import pygame
import math
import time

class Generalized_Bullet:
    def __init__(self, surface, loc_x, loc_y, vx, vy, radius, damage, is_cannonball=False, is_penetrating=False, is_bouncy=False, initial_delay=0):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.vx = vx
        self.vy = vy
        self.surface = surface
        self.radius = radius
        self.damage = damage
        self.is_cannonball = is_cannonball
        self.is_penetrating = is_penetrating
        self.is_bouncy = is_bouncy
        self.already_hit = []
        self.times_bounced = 0

        self.initial_delay = initial_delay

    def check_out_of_bounds(self):
        if self.is_bouncy:
            # bouncy mode

            if self.loc_x >= 1280:
                self.times_bounced += 1
                self.vx = -self.vx
            if self.loc_x <= 0:
                self.times_bounced += 1
                self.vx = -self.vx
            if self.loc_y >= 720:
                self.times_bounced += 1
                self.vy = -self.vy
            if self.loc_y <= 0:
                self.times_bounced += 1
                self.vy = -self.vy

        elif self.loc_x > 1300 or self.loc_x < -20 or self.loc_y > 740 or self.loc_y < -20:
            return True




    def check_collision(self,enemy):
        if self.initial_delay == 0:
            if math.sqrt((enemy.loc_x - self.loc_x)**2 + (enemy.loc_y - self.loc_y)**2) <= enemy.radius + self.radius:
                if enemy not in self.already_hit:
                    self.already_hit.append(enemy)
                    return True
                else:

                    return False
            else:

                return False
        else:
            self.initial_delay -= 1





    def check_movement(self):
        self.loc_x += self.vx
        self.loc_y += self.vy

    def render_self(self):
        pygame.draw.circle(self.surface,(255,255,204),(self.loc_x,self.loc_y),self.radius)
