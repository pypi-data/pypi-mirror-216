from .Frame import Frame
from copy import copy


class Animation:
    def __init__(self, *frames: Frame) -> None:
        self.lastUpdateTime: int = 0
        self.frameOn: int = 0
        self.frames: list[Frame] = frames
        self.current = frames[0].image

    def updateAnimation(self, ct: int) -> None:
        if ct - self.lastUpdateTime >= self.frames[self.frameOn].duration:
            self.frameOn += 1
            if self.frameOn >= len(self.frames):
                self.frameOn = 0
            self.lastUpdateTime = ct
            self.current = self.frames[self.frameOn].image

    def copy(self):
        return copy(self)
