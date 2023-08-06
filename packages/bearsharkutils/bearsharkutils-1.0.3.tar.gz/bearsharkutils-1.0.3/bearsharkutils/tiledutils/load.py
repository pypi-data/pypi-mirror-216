from .datastructures import *
from ..pygameutils.datastructures import Frame
import pytmx
from pytmx.util_pygame import load_pygame


def load(filename: str, tileSize: tuple) -> tuple[TileGroup, ObjectList]:
    tiledMap = load_pygame(filename)

    tileLayers: list[pytmx.TiledTileLayer] = [
        tilelayer
        for tilelayer in tiledMap.layers
        if isinstance(tilelayer, pytmx.TiledTileLayer)
    ]

    tileGroup = TileGroup(
        *[
            AnimatedTile(
                (x * tileSize[0], y * tileSize[1]),
                [
                    Frame(tiledMap.get_tile_image_by_gid(frame.gid), frame.duration)
                    for frame in tiledMap.get_tile_properties(x, y, layer_index)[
                        "frames"
                    ]
                ],
                tiledMap.get_tile_properties(x, y, layer_index),
                vars(layer),
            )
            if tiledMap.get_tile_properties(x, y, layer_index)["frames"]
            else VisibleTile(
                (x * tileSize[0], y * tileSize[1]),
                image,
                tiledMap.get_tile_properties(x, y, layer_index),
                vars(layer),
            )
            for layer_index, layer in enumerate(tileLayers)
            for x, y, image in layer.tiles()
        ]
    )

    objectLayer = [
        objectlayer
        for objectlayer in tiledMap.layers
        if isinstance(objectlayer, pytmx.TiledObjectGroup)
    ]

    objectList = ObjectList(
        *[
            Object(
                (vars(obj)["x"], vars(obj)["y"]),
                (vars(obj)["width"], vars(obj)["height"]),
                vars(obj),
            )
            for layer in objectLayer
            for obj in layer
        ]
    )

    return [tileGroup, objectList]
