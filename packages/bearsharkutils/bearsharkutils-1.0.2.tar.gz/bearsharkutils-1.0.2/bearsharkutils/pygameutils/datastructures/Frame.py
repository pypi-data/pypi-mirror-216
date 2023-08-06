from pygame import Surface


class Frame:
    """The `Frame` class represents a single frame of an animation with an image, rectangle, and duration."""

    def __init__(self, image: Surface, duration: int = 0) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.duration = duration
