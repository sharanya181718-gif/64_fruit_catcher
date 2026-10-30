import random
import pygame
from game.basket import Basket
from game.fruit import Fruit

class GameEngine:
    BASE_SPAWN_DELAY = 750
    MIN_SPAWN_DELAY = 250
    SCORE_PER_DIFFICULTY_LEVEL = 5
    MAX_DIFFICULTY_LEVEL = 10
    SPAWN_DELAY_DECREASE_PER_LEVEL = 50
    SPEED_INCREASE_PER_LEVEL = 0.1

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []

        self.score = 0
        self.lives = 3
        self.spawn_delay = self.BASE_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        difficulty_level = self.score // self.SCORE_PER_DIFFICULTY_LEVEL
        difficulty_level = min(difficulty_level, self.MAX_DIFFICULTY_LEVEL)
        self.spawn_delay = max(
            self.MIN_SPAWN_DELAY,
            self.BASE_SPAWN_DELAY
            - difficulty_level * self.SPAWN_DELAY_DECREASE_PER_LEVEL,
        )
        speed_multiplier = 1.0 + difficulty_level * self.SPEED_INCREASE_PER_LEVEL

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            roll = random.random()
            if roll < 0.15:
                kind = "rotten"
            elif roll < 0.30:
                kind = "bomb"
            else:
                kind = "normal"
            self.fruits.append(Fruit(self.width, kind, speed_multiplier))
            self.last_spawn_time = now

        basket_rect = self.basket.rect
        for fruit in self.fruits[:]:
            fruit.update()

            if basket_rect.colliderect(fruit.rect):
                if fruit.kind == "normal":
                    self.score += 1
                else:
                    self.lives -= 1
                self.fruits.remove(fruit)
                if self.lives == 0:
                    self.game_state = "GAME_OVER"
                    break
                continue

            if fruit.is_missed(self.height):
                if fruit.kind == "normal":
                    self.lives -= 1
                self.fruits.remove(fruit)
                if self.lives == 0:
                    self.game_state = "GAME_OVER"
                    break

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.score = 0
        self.lives = 3
        self.spawn_delay = self.BASE_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - 25
        pygame.draw.rect(screen, (45, 50, 60), (0, ground_y, self.width, 25))

        self.basket.render(screen)
        for fruit in self.fruits:
            fruit.render(screen)

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (25, 20))

        lives_surf = self.font_medium.render(f"Lives: {self.lives}", True, (240, 80, 80))
        screen.blit(lives_surf, (self.width - lives_surf.get_width() - 25, 20))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("GAME OVER", True, (235, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
