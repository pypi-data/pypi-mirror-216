"""
Property module with properties classes for the Metamaterial Analysis Code (MAC). There are one class per type of
property. They all derivative of the base class MACProperty, which is an abstract class.
"""
from abc import ABC, abstractmethod

from .MACMaterial import MACMaterial


class MACProperty(ABC):
    """
    Property class for the Metamaterial Analysis Code (MAC). It represents a single property.

    Attributes:
        ID: property ID
        Type: type of the property (PBEAM, PSOLID, etc)
        Material: list of the materials of the property
    """

    @abstractmethod
    def __init__(self, id: int, type: str, material: list[MACMaterial]):
        """
        Constructor for MACProperty class
        """
        self.__id = id
        self.__type = type
        self.__material = material

    @property
    def ID(self):
        return self.__id

    @property
    def Type(self):
        return self.__type

    @property
    def Material(self):
        return self.__material


class MACBeam(MACProperty):
    """
    Beam property class for the Metamaterial Analysis Code (MAC). It represents a single beam property.

    Attributes:
        Area: area of the beam
        I1: Area moment of inertia of the beam
        I2: Area moment of inertia of the beam
        I12: area product of inertia of the beam
        J: torsional stiffness of the beam
    """

    def __init__(self, id: int, type: str, material: list, area: float, i1: float, i2: float, i12: float, j: float):
        """
        Constructor for MACBeam class
        """
        super().__init__(id, type, material)
        self.__area = area
        self.__i1 = i1
        self.__i2 = i2
        self.__i12 = i12
        self.__j = j

    @property
    def Area(self):
        return self.__area

    @property
    def I1(self):
        return self.__i1

    @property
    def I2(self):
        return self.__i2

    @property
    def I12(self):
        return self.__i12

    @property
    def J(self):
        return self.__j

    # Method to print the property. It uses the 8 characters format of Optistruct.
    def __str__(self):

        idspaces = " " * (8 - len(str(self.ID)))
        materialspaces = " " * (8 - len(str(self.Material[0].ID)))
        area = "{:.5f}".format(self.Area)[:7]
        inertia1 = "{:.5f}".format(self.I1)[:7]
        inertia2 = "{:.5f}".format(self.I2)[:7]
        inertia12 = "{:.5f}".format(self.I12)[:7]
        torsion = "{:.5f}".format(self.J)[:7]

        return f"PBEAM   {self.ID}{idspaces}{self.Material[0].ID}{materialspaces}{area} {inertia1} {inertia2} " + \
               f"{inertia12} {torsion} \n"


class MACBeamL(MACProperty):
    """
    Beam property with a specific section. Based on the PBEAML property of optistruct.

    Attributes:
        Section: Type of section. Supported: ROD
        Dim1: First dimension. A value must be given
    """
    def __init__(self, id: int, type: str, material: list[MACMaterial], section: str, dim1: float):
        super().__init__(id, type, material)
        self.Section = section
        self.Dim1 = dim1

    # Method to print the property. It uses the 8 characters format of Optistruct.
    def __str__(self):

        idspaces = " " * (8 - len(str(self.ID)))
        materialspaces = " " * (8 - len(str(self.Material[0].ID)))
        eight = " "*8
        sectspaces = " " * (8 - len(str(self.Section)))
        dim1 = "{:.5f}".format(self.Dim1)[:7]

        return f"PBEAML  {self.ID}{idspaces}{self.Material[0].ID}{materialspaces}{eight}{self.Section}{sectspaces}\n" +\
               f"{eight}{dim1}\n"


def set_property(**kwargs) -> MACBeam | MACBeamL:
    """
    Function to create a MACProperty based object. It uses the kwargs dictionary. Supported subclasses are:
        - MACBeam:  beam = set_property(id=int, type="PBEAM", material=[MACMaterial], area=float, i1=float, i2=float, i12=float, j=float)
        - MACBeamL: beam = set_property(id=int, type="PBEAML", material=[MACMaterial], section="ROD", dim1=float)
    """

    if kwargs["type"] == "PBEAM":
        return MACBeam(id=kwargs["id"], type=kwargs["type"], material=kwargs["material"], area=kwargs["area"],
                       i1=kwargs["i1"], i2=kwargs["i2"], i12=kwargs["i12"], j=kwargs["j"])

    elif kwargs["type"] == "PBEAML":

        return MACBeamL(id=kwargs["id"], type=kwargs["type"], material=kwargs["material"], section=kwargs["section"],
                        dim1=kwargs["dim1"])

    else:
        raise ValueError("The property type is not supported.")