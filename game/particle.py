import math
import random

import pygame


class Particle:
    BACKGROUND_COLOR = (28, 32, 40)

    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 4.0)
        self.x = x
        self.y = y
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed
        self.color = color
        self.radius = random.randint(2, 4)
        self.lifetime = random.randint(24, 36)
        self.max_lifetime = self.lifetime

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.15
        self.lifetime -= 1

    def render(self, surface):
        fade = max(0, self.lifetime) / self.max_lifetime
        color = tuple(
            int(background + (foreground - background) * fade)
            for foreground, background in zip(self.color, self.BACKGROUND_COLOR)
        )
        radius = max(1, int(self.radius * fade))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)
