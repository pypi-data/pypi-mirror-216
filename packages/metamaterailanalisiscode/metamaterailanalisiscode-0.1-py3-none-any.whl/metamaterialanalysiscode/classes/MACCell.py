"""
Cell module for Metamaterial Analysis Code (MAC). It represents a single cell, made by different elements.
"""

from .MACNode import MACNode
from .MACElement import MACElement
from .MACProperty import MACProperty
from .MACMaterial import MACMaterial
from .MACStructure import MACAuxetic

class MACCell:
    """
    Cell class for Metamaterial Analysis Code (MAC). It represents a single cell, made by different elements.

    Attributes:
        ID: cell ID
        Type: type of the cell (BBC, FCC, Auxetic, etc)
        Coords: Coordinates of the center of the cell
        Size: Size of the cell
        Elements: list of elements that compose the cell
        Nodes: list of nodes that compose the cell
        Material: list of the materials of the cell
        Properties: list of the properties of the cell

    """

    def __init__(self, id: int, structure: MACAuxetic, coords: tuple, elements: tuple[MACElement], nodes: tuple[MACNode],
                 material: list[MACMaterial], properties: list[MACProperty]):
        """
        Constructor for MACCell class
        """
        self.__id = id
        self.__structure = structure
        self.__coords = coords
        self.__elements = elements
        self.__nodes = nodes
        self.__material = material
        self.__properties = properties

    @property
    def ID(self) -> int:
        return self.__id

    @property
    def Structure(self) -> str:
        return self.__structure

    @property
    def Coords(self) -> tuple:
        return self.__coords

    @property
    def Size(self) -> float:
        return self.__size

    @property
    def Elements(self) -> tuple:
        return self.__elements

    @property
    def Nodes(self) -> tuple:
        return self.__nodes

    @property
    def Material(self) -> list:
        return self.__material

    @property
    def Properties(self) -> list:
        return self.__properties

    @Elements.setter
    def Elements(self, elements) -> None:
        self.__elements = elements

