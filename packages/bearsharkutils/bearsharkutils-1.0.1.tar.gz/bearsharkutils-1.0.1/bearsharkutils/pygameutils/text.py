import pygame


def text(
    surf: pygame.Surface,
    text: str,
    size: int,
    color: tuple,
    antialias: bool,
    **rectkvargs
):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, antialias, color)
    rect = img.get_rect(**rectkvargs)
    surf.blit(img, rect)
