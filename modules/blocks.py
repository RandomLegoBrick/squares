import pygame

class Block():
    def __init__(self, position, color):
        self.rect = pygame.Rect(position)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)