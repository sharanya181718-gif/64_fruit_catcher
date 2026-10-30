import random
import pygame

class Fruit:
    MAX_SPEED_MULTIPLIER = 2.0

    def __init__(self, screen_width, kind="normal", speed_multiplier=1.0):
        self.screen_width = screen_width
        self.kind = kind
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2
        speed_multiplier = min(
            max(speed_multiplier, 1.0),
            self.MAX_SPEED_MULTIPLIER,
        )
        self.speed = random.uniform(4.0, 6.5) * speed_multiplier
        if self.kind == "rotten":
            self.color = (100, 75, 35)
        elif self.kind == "bomb":
            self.color = (35, 35, 40)
        else:
            self.color = random.choice([
                (230, 45, 45),   # Apple
                (245, 140, 30),  # Orange
                (160, 60, 200),  # Grape
            ])

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))
        if self.kind == "bomb":
            pygame.draw.circle(surface, self.color, center, self.radius)
            pygame.draw.circle(surface, (180, 180, 185), center, self.radius, 2)
            pygame.draw.line(
                surface,
                (230, 190, 80),
                (center[0], center[1] - self.radius),
                (center[0] + 5, center[1] - self.radius - 7),
                3,
            )
            pygame.draw.circle(
                surface,
                (255, 90, 30),
                (center[0] + 6, center[1] - self.radius - 8),
                3,
            )
            return

        pygame.draw.circle(surface, self.color, center, self.radius)
        highlight_color = (
            (75, 55, 30) if self.kind == "rotten" else (255, 255, 255)
        )
        pygame.draw.circle(
            surface,
            highlight_color,
            (int(self.x - 4), int(self.y - 4)),
            3,
        )
        if self.kind == "rotten":
            pygame.draw.circle(
                surface,
                (55, 45, 25),
                (int(self.x + 5), int(self.y + 4)),
                3,
            )