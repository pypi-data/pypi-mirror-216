from pygame import Rect
from pygame.sprite import Sprite


class Tile(Sprite):
    """This is a class for creating tiles in a game with properties and layer properties."""

    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        props: dict,
        layerProps: dict,
        *groups
    ) -> None:
        super().__init__(*groups)
        self.rect = Rect(*pos, *size)
        self.props = props
        self.layerProps = layerProps
