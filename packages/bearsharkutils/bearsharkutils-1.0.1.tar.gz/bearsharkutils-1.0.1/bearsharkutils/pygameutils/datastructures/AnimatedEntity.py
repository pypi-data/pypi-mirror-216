from .Entity import Entity
from .Animation import Animation


class AnimatedEntity(Entity):
    def __init__(
        self, pos: tuple[int, int], animations: list[Animation], *groups
    ) -> None:
        self.animations = animations
        super().__init__(pos, animations[0].current, *groups)

    def updateAnimation(self, ct: int):
        for animation in self.animations:
            animation.updateAnimation(ct)
