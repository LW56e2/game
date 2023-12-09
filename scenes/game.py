import pygame
import sys
import random

import util
from classes import Player
from classes import Generalized_Bullet
from classes import Enemy
import os
import math

class Game:
    def __init__(self):
        # Initialize Pygame and set up the screen, fonts, etc.
        base_dir = os.path.dirname(__file__)  # points to directory of where the code is running
        font_file_path = os.path.join(base_dir, '../assets/coolvetica_regular.otf')

        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.font_1 = pygame.font.Font(font_file_path, 40)

        self.clock = pygame.time.Clock()
        self.running = True
        self.alive = True

        self.bullet_list = []
        self.enemy_list = []

        self.classes = ["Tank", "Scout", "Shotgunner", "Exploder", "Sniper", "Cannoneer", "Sprayer", "Archer"]

        pygame.display.set_caption('A Game!')

        self.player = Player(self.screen, 640, 360)


    def choose_class(self):
        # Display class options
        self.screen.fill((0, 0, 0))  # Filling screen with black
        for i, class_name in enumerate(self.classes):
            text = self.font_1.render(class_name+f' - Select {i+1}', True, (255, 255, 255))
            self.screen.blit(text, (50, 50 + (30+20) * i))

        pygame.display.flip()

        # Event handling for class selection
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choosing = False
                    self.running = False
                # region classes attributes
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        # tank
                        self.player.chosen_class = self.classes[0]
                        self.player.speed = 2.2
                        self.player.radius = 40
                        self.player.bullet_speed = 30
                        self.player.gun_length = 35
                        self.player.gun_width = 25
                        self.player.shots_per_second = 2.2
                        self.player.health = 800
                        self.player.points = 0
                        self.player.bullet_radius = 30
                        self.player.damage = 30

                    elif event.key == pygame.K_2:
                        # scout
                        self.player.chosen_class = self.classes[1]
                        self.player.speed = 8
                        self.player.radius = 20
                        self.player.bullet_speed = 10
                        self.player.gun_length = 18
                        self.player.gun_width = 8
                        self.player.shots_per_second = 10
                        self.player.health = 100
                        self.player.points = 0
                        self.player.bullet_radius = 10
                        self.player.damage = 12

                    elif event.key == pygame.K_3:
                        # shotgunner

                        self.player.chosen_class = self.classes[2]
                        self.player.speed = 3
                        self.player.radius = 25
                        self.player.bullet_speed = 12
                        self.player.gun_length = 30
                        self.player.gun_width = 10
                        self.player.shots_per_second = 1.5
                        self.player.health = 120
                        self.player.points = 0
                        self.player.bullet_radius = 8
                        self.player.damage = 5

                    elif event.key == pygame.K_4:
                        # exploder

                        self.player.chosen_class = self.classes[3]

                        self.player.speed = 3
                        self.player.radius = 25
                        self.player.bullet_speed = 20
                        self.player.gun_length = 40
                        self.player.gun_width = 20
                        self.player.shots_per_second = 4
                        self.player.health = 120
                        self.player.points = 0
                        self.player.bullet_radius = 12
                        self.player.damage = 3

                    elif event.key == pygame.K_5:
                        # Sniper
                        self.player.chosen_class = self.classes[4]
                        self.player.speed = 4
                        self.player.radius = 25
                        self.player.bullet_speed = 40
                        self.player.gun_length = 32
                        self.player.gun_width = 12
                        self.player.shots_per_second = 2.3
                        self.player.health = 80
                        self.player.points = 0
                        self.player.bullet_radius = 6
                        self.player.damage = 100

                    elif event.key == pygame.K_6:
                        self.player.chosen_class = self.classes[5]
                        # Cannoneer
                        self.player.speed = 2.4
                        self.player.radius = 30
                        self.player.bullet_speed = 20
                        self.player.gun_length = 40
                        self.player.gun_width = 30
                        self.player.shots_per_second = 3
                        self.player.health = 50
                        self.player.points = 0
                        self.player.bullet_radius = 40
                        self.player.damage = 1
                        self.player.bullet_is_cannonball = True
                    elif event.key == pygame.K_7:
                        self.player.chosen_class = self.classes[6]
                        # Sprayer
                        self.player.speed = 4
                        self.player.radius = 35
                        self.player.bullet_speed = 10
                        self.player.gun_length = 20
                        self.player.gun_width = 30
                        self.player.shots_per_second = 60
                        self.player.health = 100
                        self.player.points = 0
                        self.player.bullet_radius = 15
                        self.player.damage = 2

                    elif event.key == pygame.K_8:
                        self.player.chosen_class = self.classes[7]
                        # Archer
                        self.player.speed = 3.5
                        self.player.radius = 30
                        self.player.bullet_speed = 25
                        self.player.gun_length = 40
                        self.player.gun_width = 20
                        self.player.shots_per_second = 4
                        self.player.health = 140
                        self.player.points = 0
                        self.player.bullet_radius = 20
                        self.player.damage = 20
                        self.player.bullet_is_penetrating = True
                        self.player.bullet_is_bouncy = True
                    else:
                        sys.exit(1)
                    # Add more key bindings for other classes as needed
                    choosing = False
                # endregion

        self.main_game_loop()




    def main_game_loop(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            self.screen.fill((0, 0, 0)) # black background

            # RENDER YOUR GAME HERE

            # region player calculations

            if self.player.check_death():
                self.show_death_screen()


            self.player.check_movement()
            self.player.render_self()

            # endregion

            # region enemy spawn calculations

            health_multiplier = 1 + self.player.points / 100
            if 90 - self.player.points >= 20:
                options_to_choose_from = 90 - self.player.points
            else:
                options_to_choose_from = 20
            if random.randint(1, options_to_choose_from) == 1:
                enemy_spawn_x = random.randint(0, 1280)
                enemy_spawn_y = random.randint(0, 720)
                if math.sqrt((enemy_spawn_x-self.player.loc_x)**2 + (enemy_spawn_y-self.player.loc_y)**2) >= 300:

                    self.enemy_list.append(Enemy(self.screen, enemy_spawn_x, enemy_spawn_y, 0, 0, round(60*health_multiplier)))
            # endregion


            # region bullet calculations
            shots = self.player.check_shoot(self.screen)
            if shots:
                for bullet in shots:
                    self.bullet_list.append(bullet)

            bullets_to_remove = []
            for bullet in self.bullet_list:
                if bullet != None:
                    if bullet.is_bouncy:
                        bullet.check_out_of_bounds()  # bouncy mode
                        if len(bullet.already_hit) >= 3:
                            bullets_to_remove.append(bullet)
                        elif bullet.times_bounced >= 5:
                            bullets_to_remove.append(bullet)

                    elif bullet.check_out_of_bounds():
                        bullets_to_remove.append(bullet)


                    bullet.render_self()
                    bullet.check_movement()

                    for enemy in self.enemy_list:
                        if bullet.check_collision(enemy):
                            enemy.health -= self.player.damage
                            if bullet.is_penetrating == False:
                                bullets_to_remove.append(bullet)

                            if bullet.is_cannonball:
                                all_vectors = util.create_circular_normalized_vectors(12)
                                for vector in all_vectors:
                                    if vector:
                                        if bullet.radius >= 40:
                                            self.bullet_list.append(Generalized_Bullet(bullet.surface, bullet.loc_x, bullet.loc_y,
                                                                                       vector[0] * self.player.bullet_speed,
                                                                                vector[1] * self.player.bullet_speed, bullet.radius/2, bullet.damage/4,
                                                                                       initial_delay=6,is_cannonball=True))
                                        else:
                                            self.bullet_list.append(Generalized_Bullet(bullet.surface, bullet.loc_x, bullet.loc_y,
                                                                                       vector[0] * self.player.bullet_speed,
                                                                                       vector[1] * self.player.bullet_speed, bullet.radius / 2,
                                                                                       bullet.damage / 4,
                                                                                       initial_delay=6, is_cannonball=False))




                else:
                    bullets_to_remove.append(bullet) # add to list to avoid removing bullets multiple times

            # remove bullets
            for bullet_to_remove in bullets_to_remove:
                if bullet_to_remove in self.bullet_list:
                    self.bullet_list.remove(bullet_to_remove)
            # endregion

            # region enemy calculations
            enemies_to_remove = []
            for enemy in self.enemy_list:
                if enemy.check_death():
                    enemies_to_remove.append(enemy)
                enemy.check_movement()
                enemy.render_self()
                enemy.move_to_player(self.player.loc_x, self.player.loc_y)
                self.player.health -= enemy.check_collision(self.player.loc_x, self.player.loc_y, self.player.radius)
            for enemy_to_remove in enemies_to_remove:
                self.enemy_list.remove(enemy_to_remove)
                self.player.points += 1
            # endregion

            # region Health display
            text = self.font_1.render('Health: ' + str(self.player.health), True, (255, 80, 80))
            textRect = text.get_rect()
            textRect.left = 10
            textRect.bottom = 710
            self.screen.blit(text, textRect)
            # endregion

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
        pygame.quit()



    def show_death_screen(self):
        self.screen.fill((255,0,0))
        death_text = self.font_1.render(f"You Died. You got {self.player.points} points. Press Q to Quit", True, (255,255,255))
        text_rect = death_text.get_rect(center=(1280 / 2, 720 / 2))
        self.screen.blit(death_text, text_rect)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print('R')
                        self.main_game_loop()  # Restart game

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()



