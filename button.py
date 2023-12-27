import pygame


class Button:

    def __init__(self, window, pathway: str, x, y, width=None, height=None, hover_pathway=None):
        self.window = window
        if not width and not height and hover_pathway:
            self.image = pygame.image.load(pathway)
            self.hover_image = pygame.image.load(hover_pathway)
        elif not width and not height:
            self.image = pygame.image.load(pathway)
            self.hover_image = self.image
        elif hover_pathway:
            self.image = pygame.transform.scale(
                pygame.image.load(pathway), (width, height))
            self.hover_image = pygame.transform.scale(
                pygame.image.load(hover_pathway), (width, height))
        elif width and height:
            self.image = pygame.transform.scale(
                pygame.image.load(pathway), (width, height))
            self.hover_image = self.image

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_mouse_hov(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return 0 < mouse_x - self.x < self.width and 0 < mouse_y - self.y < self.height

    def is_clicked_on(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.is_mouse_hov() and pygame.mouse.get_pressed()[0]

    def draw(self):
        if self.is_mouse_hov():
            self.window.blit(self.hover_image, (self.x, self.y))
        else:
            self.window.blit(self.image, (self.x, self.y))
