from typing import Literal
from .Object import Object


class ObjectList(list[Object]):
    """The ObjectList class allows for searching objects based on their properties."""

    def __init__(self, *args: Object):
        super().__init__(args)

    def search_by_props(
        self: list[Object],
        key: Literal[
            "name",
            "type",
            "x",
            "y",
            "width",
            "height",
            "rotation",
            "gid",
            "visible",
            "image",
            "properties",
        ],
        value,
    ):
        """
        This function searches for objects in a ObjectList based on their properties, such as gid or type.
        """
        istype = lambda obj: obj.props[key] == value

        filteredList = ObjectList(*filter(istype, self))

        return filteredList
