from .AnimatedEntity import AnimatedEntity
from pygame.sprite import Group


class AnimatedEntityGroup(Group):
    def __init__(self, *sprites: list[AnimatedEntity]) -> None:
        super().__init__(*sprites)

    def updateAnimation(self, ct):
        entity: AnimatedEntity
        for entity in self.sprites():
            if isinstance(entity, AnimatedEntity):
                entity.updateAnimation(ct)
