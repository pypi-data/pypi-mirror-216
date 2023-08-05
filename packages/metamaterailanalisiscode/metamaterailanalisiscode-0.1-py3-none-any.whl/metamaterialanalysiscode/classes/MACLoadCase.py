"""
Module with the MACLoadCase base class and its derived classes.
"""
from MetamaterialAnalysisCode.classes.MACNode import MACNode


class MACLoadCase:
    """
    Base class for the load cases. Supported classes: FORCE, SPC, EIGRL.

    Attributes:
        ID: load case ID
        Type: load case type
    """

    def __init__(self, id_: int, type_: str):
        """
        Constructor for MACLoadCase class
        """
        self.ID = id_
        self.Type = type_


class MACForce(MACLoadCase):
    """
    Class for the FORCE load case. It derives from MACLoadCase.

    Attributes:
        ID: load case ID
        Type: load case type
        Node/Set: node where the force is applied/Set of nodes where the force is applied
        Direction: direction of the force
        Magnitude: magnitude of the force
        GSet: bool that is True if the force is applied to a set of nodes, False otherwise
    """

    def __init__(self, id_: int, node: list[MACNode, ...], direction: tuple[float, float, float], magnitude: float):
        """
        Constructor for MACForce class
        """
        super().__init__(id_, "FORCE")
        self.Nodes = node
        self.Direction = direction
        self.Magnitude = magnitude
        if len(node) > 1:
            self.__gset = True
        else:
            self.__gset = False

    def __str__(self):
        """
        Method to print a FORCE load case. It uses the 8 characters format of Optistruct.
        """
        idspaces = " " * (8 - len(str(self.ID)))
        systemspaces = " " * 8

        # 8 characters for each coordinate. It uses scientific notation with 3 decimal places.
        x = "{:.5f}".format(self.Direction[0])[:7]
        y = "{:.5f}".format(self.Direction[1])[:7]
        z = "{:.5f}".format(self.Direction[2])[:7]
        magnitude = "{:.5f}".format(self.Magnitude)[:7]

        if self.GSet:
            idset = str(self.ID*100)
            idspaceset = " " * (8 - len(str(idset)))
            gset = f"SET     {idset}{idspaceset}    GRID    LIST\n" + " "*8
            count = 0

            for node in self.Nodes:
                nodespaces = " " * (8 - len(str(node.ID)))
                gset += f"{nodespaces}{node.ID}"
                count += 1
                if count == 8:
                    gset += "\n" + " "*8
                    count = 0
            gset += "\n"

            return f"FORCE   {idspaces}{self.ID}{idspaceset}{idset}{systemspaces} {magnitude}" + \
                   f" {x} {y} {z}\n" + " "*8 + "GSET" + "\n" + gset
        else:
            nodespaces = " " * (8 - len(str(self.Nodes[0].ID)))
            return f"FORCE   {idspaces}{self.ID}{nodespaces}{self.Nodes[0].ID}{systemspaces}{magnitude}" + \
                   f" {x} {y} {z}\n"

    @property
    def GSet(self) -> bool:
        """
        If True, the force is applied to a set of nodes, if False, the force is applied to a single node.
        """
        return self.__gset


class MACSpc(MACLoadCase):
    """
    Class for the SPC load case. It derives from MACLoadCase.

    Attributes:
        ID: load case ID
        Type: load case type
        Node/Set: node where the force is applied/Set of nodes where the force is applied
        Components: Freedom degrees that are constrained
        Displacement: Value of enforced displacement for all coordinates
        GSet: bool that is True if the force is applied to a set of nodes, False otherwise
    """

    def __init__(self, id_: int, node: list[MACNode, ...], components: list[int, ...], displacement: float,
                 enfdisp: bool = False):
        """
        Constructor for MACSPC class
        """
        super().__init__(id_, "SPC")
        self.Nodes = node
        self.Components = components
        self.Displacement = displacement
        self.EnfDisp = enfdisp  # Enforced Displacement
        if len(node) > 1:
            self.__gset = True
        else:
            self.__gset = False

    @property
    def GSet(self) -> bool:
        """
        If True, the force is applied to a set of nodes, if False, the force is applied to a single node.
        """
        return self.__gset

    def __str__(self):
        """
        Method to print a SPC load case. It uses the 8 characters format of Optistruct.
        """
        idspaces = " " * (8 - len(str(self.ID)))

        # 8 characters for each coordinate. It uses scientific notation with 3 decimal places.
        displacement = "{:.5f}".format(self.Displacement)[:7]
        components = ""
        for comp in self.Components:
            components += str(comp)
        compspaces = " " * (8 - len(components))

        if self.GSet:
            idset = str(self.ID*100+self.Nodes[0].ID)
            idspaceset = " " * (8 - len(str(idset)))
            gset = f"SET     {idspaceset}{idset}    GRID    LIST\n" + " "*8
            count = 0

            for node in self.Nodes:
                nodespaces = " " * (8 - len(str(node.ID)))
                gset += f"{nodespaces}{node.ID}"
                count += 1
                if count == 8:
                    gset += "\n" + " "*8
                    count = 0
            gset += "\n"

            if self.EnfDisp:
                return f"SPCD    {idspaces}{self.ID}{idspaceset}{idset}{compspaces}{components} {displacement}\n" + \
                       " " * 8 + "    GSET" + "\n" + gset

            else:
                return f"SPC     {idspaces}{self.ID}{idspaceset}{idset}{compspaces}{components} {displacement}\n" + \
                   " "*8 + "    GSET" + "\n" + gset

        else:

            nodespaces = " " * (8 - len(str(self.Nodes[0].ID)))

            if self.EnfDisp:
                idspcadd = str(self.ID * 100 + 1)
                spcaddspaces = " " * (8 - len(str(idspcadd)))
                return f"SPCD    {spcaddspaces}{idspcadd}{nodespaces}{self.Nodes[0].ID}{compspaces}{components} " + \
                       f"{displacement}\n"

            else:
                return f"SPC     {self.ID}{idspaces}{nodespaces}{self.Nodes[0].ID}{compspaces}{components} " + \
                       f"{displacement}\n"


class MACEigrl(MACLoadCase):
    """
    Class for the EIGRL load case. It derives from MACLoadCase.

    Attributes:
        ID: load case ID
        Type: load case type
        NumRoots: number of roots to be calculated
    """

    def __init__(self, id_: int, numroots: int):
        """
        Constructor for MACEigrl class
        """
        super().__init__(id_, "EIGRL")
        self.NumRoots = numroots

    def __str__(self):
        """
        Method to print an EIGRL load case. It uses the 8 characters format of Optistruct.
        """
        idspaces = " " * (8 - len(str(self.ID)))
        numrootsspaces = " " * (8 - len(str(self.NumRoots)))
        vibrationspaces = " " * 8 * 2
        return f"EIGRL   {idspaces}{self.ID}{vibrationspaces}{numrootsspaces}{self.NumRoots}\n"


def set_load(**kwargs) -> MACForce | MACSpc:
    """
    Function to set the load case. It could return a MACForce, MACSpc or MACEigrl. Its arguments should be given as
    keyword arguments:
        - MACForce: set_load_case(id=int, type="FORCE" nodes=[MACNode], direction=tuple[float, ...], magnitude=float)
        - MACSpc: set_load_case(id=int, type="SPC" nodes=[MACNode], components=list[int, ...], displacement=float)
        - MACEigrl: set_load_case(id=int, type="EIGRL", numroots=int)
    """

    if kwargs["type"] == "FORCE":
        load_case = MACForce(kwargs["id"], kwargs["nodes"], kwargs["direction"], kwargs["magnitude"])

    elif kwargs["type"] == "SPC":
        load_case = MACSpc(kwargs["id"], kwargs["nodes"], kwargs["components"], kwargs["displacement"],
                           kwargs.get("load", True))

    else:
        raise ValueError("Invalid LOAD type")

    return load_case


def set_constraint(id: int, nodes: list[MACNode, ...], components: list[int, ...], displacement: float,
                   load: bool = False) -> MACSpc:
    """
    Function to set the constraint load case. It returns a MACSpc.
        - MACSpc: set_load_case(id=int, nodes=[MACNode], components=list[int, ...], displacement=float,
                                load=bool)
    """
    return MACSpc(id, nodes, components, displacement, load)


def set_eigr(id: int, type: str, numroots: int) -> MACEigrl:
    """
    Function to set the EIGRL load case. It returns a MACEigrl.
        - MACEigrl: set_load_case(id=int, type="EIGRL", numroots=int)
    """
    if type == "EIGRL":
        return MACEigrl(id, numroots)
    else:
        raise ValueError("Invalid EIGR type")