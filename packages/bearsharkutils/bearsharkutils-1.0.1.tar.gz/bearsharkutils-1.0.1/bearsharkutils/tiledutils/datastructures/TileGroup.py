from pygame.sprite import Group
from typing import Literal
from .AnimatedTile import AnimatedTile
from .Tile import Tile


class TileGroup(Group):
    """The TileGroup class is a subclass of pygame.sprite.Group that allows searching for sprites based on
    their types and layer properties."""

    def __init__(self, *sprites: Tile) -> None:
        super().__init__(*sprites)

    def search_by_type(self, value):
        """
        This function searches for sprites in a TileGroup based on their type.
        """
        filteredGroup = TileGroup()

        sprite: Tile
        for sprite in self.sprites():
            if sprite.props["type"] == value:
                filteredGroup.add(sprite)

        return filteredGroup

    def search_by_layerProps(
        self,
        key: Literal["name", "visible"],
        value,
    ):
        """
        This function searches for sprites in a TileGroup based on their layer properties matching a given
        key-value pair.
        """
        filteredGroup = TileGroup()

        sprite: Tile
        for sprite in self.sprites():
            if sprite.layerProps[key] == value:
                filteredGroup.add(sprite)

        return filteredGroup

    def updateAnimation(self, ct):
        for tile in self.sprites():
            if isinstance(tile, AnimatedTile):
                tile.updateAnimation(ct)
