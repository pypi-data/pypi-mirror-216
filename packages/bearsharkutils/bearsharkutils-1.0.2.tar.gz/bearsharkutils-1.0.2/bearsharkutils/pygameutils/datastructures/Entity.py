from pygame import Surface
from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, pos: tuple[int, int], image: Surface, *groups) -> None:
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect(center=pos)
