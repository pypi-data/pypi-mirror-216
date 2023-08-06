from pygame import Rect


class Object:
    def __init__(
        self, pos: tuple[int, int], size: tuple[int, int], props: dict
    ) -> None:
        self.rect = Rect(*pos, *size)
        self.props = props
