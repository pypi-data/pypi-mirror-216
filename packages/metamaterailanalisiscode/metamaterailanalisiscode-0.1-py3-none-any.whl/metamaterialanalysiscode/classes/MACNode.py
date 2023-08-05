"""
Node module for the Metamaterial Analysis Code (MAC). It represents a single grid.
"""


class MACNode:
    """
    Node class for the Metamaterial Analysis Code (MAC). It represents a single grid.

    Attributes:
        ID: node ID
        Coords: Coordinates of the node
    """

    def __init__(self, id_: int, coords: tuple[float, ...]):
        """
        Constructor for MACNode class
        """
        self.__id = id_
        self.__coords = coords

    @property
    def ID(self):
        return self.__id

    @property
    def Coords(self) -> tuple:
        return self.__coords

    @Coords.setter
    def Coords(self, value):
        self.__coords = value

    # Method to compare two nodes. It returns True if the nodes are the same (they have the same coordinates),
    # False otherwise.
    def __eq__(self, other) -> bool:
        if isinstance(other, MACNode):
            return self.Coords == other.Coords
        else:
            return False

    # Method to hash a node. It uses the coordinates of the node as hash to be implemented in a set.
    def __hash__(self):
        return hash((self.Coords[0], self.Coords[1], self.Coords[2], self.ID))

    # Method to print a node. It uses the 8 characters format of Optistruct.
    def __str__(self):

        idspaces = " " * (8 - len(str(self.ID)))
        systemspaces = " " * 8

        # 8 characters for each coordinate. It uses scientific notation with 3 decimal places.
        x = "{:.5f}".format(self.Coords[0])[:7]
        y = "{:.5f}".format(self.Coords[1])[:7]
        z = "{:.5f}".format(self.Coords[2])[:7]

        return f"GRID    {idspaces}{self.ID}{systemspaces} {x} {y} {z}\n"
