import arcade
import pygame
import random
import time
import numpy
import cv2
import PIL


class Gamerendering:
    def __init__(self, velocity, new_window=True):
        self.velocity = velocity

        self.width = 525
        self.height = 675
        if new_window:
            arcade.open_window(self.width, self.height, "Flappy Bird")

        self.players = []
        self.sprite_players = arcade.SpriteList()

        self.pipes = []
        self.sprite_pipes = arcade.SpriteList()

        self.sprite_background = arcade.sprite.Sprite("Images/background.png", 1.5, center_x=263, center_y=337)
        self.black_background = arcade.sprite.Sprite("Images/black.jpg", center_x=self.width // 2,
                                                     center_y=self.height // 2,
                                                     image_height=self.height, image_width=self.width)

        self.sprite_foreground = arcade.SpriteList()
        self.sprite_foreground.append(arcade.sprite.Sprite("Images/foreground.jpg", 1.5, center_x=375, center_y=30))
        self.sprite_foreground.append(arcade.sprite.Sprite("Images/foreground.jpg", 1.5, center_x=1128, center_y=30))

    def reset(self, velocity):
        self.__init__(velocity, new_window=False)

    def add_player(self, player):
        self.players.append(player)
        self.sprite_players.append(
            arcade.sprite.Sprite("Images/bird_yellow.png", 0.2, center_x=player.x_pos, center_y=player.y_pos))

    def _get_image(self):
        print(self.black_background)
        self.black_background.draw()
        self._draw_pipes()
        self._draw_players()
        image = arcade.get_image(0, 0, self.width, self.height)
        # image = image.convert('RGB')
        # image.show()
        # image = numpy.array(image)
        # gray = cv2.cvtColor(image[30:490, 0:400], cv2.COLOR_BGR2GRAY)
        # PIL.Image.fromarray(gray1).show()
        # gray = cv2.cvtColor(image[30:490, 0:400], cv2.COLOR_RGB2GRAY)
        return image

    # Adding pipe to be rendered
    def add_pipe(self, pipe):
        self.pipes.append(pipe)
        self.sprite_pipes.append(arcade.Sprite("Images/pipe_down.png", 0.3))
        self.sprite_pipes[-1].left = pipe.x_pos
        self.sprite_pipes[-1].top = pipe.y_pos
        self.sprite_pipes.append(arcade.Sprite("Images/pipe_up.png", 0.3))
        self.sprite_pipes[-1].left = pipe.x_pos
        self.sprite_pipes[-1].bottom = pipe.y_pos + pipe.opening_width

    # Drawing pipes
    def _draw_pipes(self):
        # Looping through all pairs of pipes
        for x in range(len(self.pipes)):
            # Bottom-pipe
            self.sprite_pipes[2 * x].left = self.pipes[x].x_pos
            self.sprite_pipes[2 * x].top = self.pipes[x].y_pos
            self.sprite_pipes[2 * x].draw()

            # Top-pipe
            self.sprite_pipes[2 * x + 1].left = self.pipes[x].x_pos
            self.sprite_pipes[2 * x + 1].bottom = self.pipes[x].y_pos + self.pipes[x].opening_width
            self.sprite_pipes[2 * x + 1].draw()

    # Drawing players
    def _draw_players(self):
        # Looping through all players
        for x in range(len(self.players) - 1, -1, -1):
            # Quit rendering this player
            if self.players[x].delete_from_render:
                self.players[x].delete_from_render = False
                self.sprite_players.remove(self.sprite_players[x])
                del self.players[x]
                continue
            # Rendering the player
            self.sprite_players[x].center_x = self.players[x].x_pos
            self.sprite_players[x].center_y = self.players[x].y_pos
            self.sprite_players[x].angle = self.players[x].angle
            self.sprite_players[x].draw()
            # # Marking alive and dead birds
            # if self.players[x].alive:
            #     arcade.draw_circle_filled(self.players[x].x_pos, self.players[x].y_pos, self.players[x].radius, arcade.color.YELLOW)
            # else:
            #     arcade.draw_circle_filled(self.players[x].x_pos, self.players[x].y_pos, self.players[x].radius,
            #                               arcade.color.RED)

    # Main function for rendering a frame
    def draw(self, pipes_passed, current_fitness, players_alive, velocity, generation, return_image=False):
        self.velocity = velocity

        arcade.start_render()
        # Draw background
        image = self._get_image() if return_image else None

        self.sprite_background.draw()

        # Draw pipes
        self._draw_pipes()

        # Draw players
        self._draw_players()

        # Draw foreground
        for im in self.sprite_foreground:
            if im.center_x < -375:
                im.center_x = 1128
            im.center_x -= self.velocity
            im.draw()
        # Draw text
        arcade.draw_text(str(pipes_passed), 250, 580, arcade.color.WHITE, 80, align="center",
                         anchor_x="center")
        arcade.draw_text("Current fitness: " + str(current_fitness), 10, 100, arcade.color.WHITE, 20)
        arcade.draw_text("Players alive: " + str(players_alive), 10, 80, arcade.color.WHITE, 20)
        arcade.draw_text("Generation: " + str(generation), 10, 60, arcade.color.WHITE, 20)
        arcade.finish_render()

        if return_image:
            # PIL.Image.fromarray(image).show()
            return image
        return None
