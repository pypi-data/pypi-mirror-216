"""
Element module for the Metamaterial Analysis Code (MAC). It represents a single element.
"""

from .MACNode import MACNode
from .MACProperty import MACProperty
from .MACMaterial import MACMaterial

class MACElement:
    """
    Element class for the Metamaterial Analysis Code (MAC). It represents a single element.

    Attributes:
        ID: element ID
        Type: type of the element (CBEAM, CQUAD, etc)
        Nodes: list of nodes that compose the element
        Material: list of the materials of the element
        Properties: list of the properties of the element
        Vvector: vector that determines the orientation of the element

    """

    def __init__(self, id_: int, type_: str, nodes: list[MACNode], material: list[MACMaterial],
                 properties: list[MACProperty], vvector: tuple, aux: bool = False):
        """
        Constructor for MACElement class
        """
        self.__id = id_
        self.__type = type_
        self.__nodes = nodes
        self.__material = material
        self.__properties = properties
        self.__vvector = vvector
        self.Aux = aux  # Propiedad auxiliar para saber si es de los elementos que se pueden borrar

    @property
    def ID(self):
        return self.__id

    @property
    def Type(self):
        return self.__type

    @property
    def Nodes(self):
        return self.__nodes

    @property
    def Materials(self):
        return self.__material

    @property
    def Property(self):
        return self.__properties

    @property
    def Vvector(self):
        return self.__vvector

    # Method to print a node. It uses the 8 characters format of Optistruct.
    def __str__(self):

        match self.Type:

            case "CBEAM":

                idspaces = " " * (8 - len(str(self.ID)))
                propspaces = " " * (8 - len(str(self.Property[0].ID)))
                node0spaces = " " * (8 - len(str(self.Nodes[0].ID)))
                node1spaces = " " * (8 - len(str(self.Nodes[1].ID)))
                vv0spaces = " " * (8 - len(str(self.Vvector[0])))
                vv1spaces = " " * (8 - len(str(self.Vvector[1])))
                vv2spaces = " " * (8 - len(str(self.Vvector[2])))

                return f"CBEAM   {idspaces}{self.ID}{propspaces}{self.Property[0].ID}{node0spaces}{self.Nodes[0].ID}" + \
                       f"{node1spaces}{self.Nodes[1].ID}{vv0spaces}{self.Vvector[0]}{vv1spaces}{self.Vvector[1]}" + \
                       f"{vv2spaces}{self.Vvector[2]}\n"

            case "CQUAD":

                return "CQUAD is not yet implemented"

    def __hash__(self):
        return hash(self.ID)