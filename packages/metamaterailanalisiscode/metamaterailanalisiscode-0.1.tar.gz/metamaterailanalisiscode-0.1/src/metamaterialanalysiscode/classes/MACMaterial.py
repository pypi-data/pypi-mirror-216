"""
Material module for Metamaterial Analysis Code (MAC). It represents a single material.
"""
from typing import Any
from abc import ABC, abstractmethod

from MetamaterialAnalysisCode.classes.MACTable import MACTable

class MACMaterial(ABC):
    """
    Material base class for Metamaterial Analysis Code (MAC). The materials classes (MACMatNL or MACMat) are based
    on this base class

    Attributes:
        ID: material ID
        Type: type of the material (Supported: MATS1)
    """
    @abstractmethod
    def __init__(self, id_: int, type_: str):
        """
        Constructor for MACMaterial class
        """
        self.ID = id_
        self.Type = type_


class MACMatNL(MACMaterial):
    """
    Non-Linear Material class for Metamaterial Analysis Code (MAC). It represents a single material.

    Attributes:
        ID: material ID
        StressStrain: stress-strain curve of the material
        Type: type of the material (Supported: MATS1)
        NonLinearity: type of non-linearity of the material (LINEAR, PLASTIC, NLELAST)
        YieldStress: Stress at the yield point in the strain-stress curve of the material
    """

    def __init__(self, id_: int, type_: str, stressstrain: MACTable = None, nonlinearity: str = "PLASTIC",
                 yieldstress: float = 0.0):
        """
        Constructor for MACMaterial class
        """
        super().__init__(id_, type_)
        self.StressStrain = stressstrain
        self.NonLinearity = nonlinearity
        self.YieldStress = yieldstress

    # Method to print a node. It uses the 8 characters format of Optistruct.
    def __str__(self):

        idspaces = " " * (8 - len(str(self.ID)))
        stressspaces = " " * (8 - len(str(self.StressStrain.ID)))
        nonlinearityspaces = " " * (8 - len(self.NonLinearity))

        return f"MATS1   {self.ID}{idspaces}{self.StressStrain.ID}{stressspaces}{self.NonLinearity}" + \
               f"{nonlinearityspaces}\n" + "\n" + " " * 8 + f"{self.YieldStress}\n"


class MACMat(MACMaterial):
    """
    Linear isotropic Material class for Metamaterial Analysis Code (MAC). It represents a single material.

    Attributes:
        ID: material ID
        Type: MAT1
        E: Young's modulus
        G: Shear modulus
        Nu: Poisson's ratio
        Rho: Density
        TExp: Thermal expansion coefficient
        TRef: Reference temperature
        GE: Structural damping coefficient
        ST: Stress limit for tension
        SC: Stress limit for compression
        SS: Stress limit for shear
    """

    def __init__(self, id_: int, type_: str, e: float, nu: float, g: float = None, rho: float = None,
                 texp: float = None, tref: float = None, ge: float = None,
                 st: float = None, sc: float = None, ss: float = None):
        """
        Constructor for MACMat class
        """
        super().__init__(id_, type_)
        self.E = e
        self.G = g
        self.Nu = nu
        self.Rho = rho
        self.TExp = texp
        self.TRef = tref
        self.GE = ge
        self.ST = st
        self.SC = sc
        self.SS = ss

    def __str__(self):

        idspaces = " " * (8 - len(str(self.ID)))
        e = "{:.5f}".format(self.E)[:7]
        nu = "{:.5f}".format(self.Nu)[:7]

        if self.G is None:
            g = " "*7
        else:
            g = "{:.5f}".format(self.G)[:7]

        if self.Rho is None:
            rho = " "*7
        else:
            rho = "{:.5f}".format(self.Rho)[:7]

        if self.TExp is None:
            texp = " "*7
        else:
            texp = "{:.5f}".format(self.TExp)[:7]

        if self.TRef is None:
            tref = " "*7
        else:
            tref = "{:.5f}".format(self.TRef)[:7]

        if self.GE is None:
            ge = " "*7
        else:
            ge = "{:.5f}".format(self.GE)[:7]

        if self.ST is None:
            st = " "*7
        else:
            st = "{:.5f}".format(self.ST)[:7]

        if self.SC is None:
            sc = " "*7
        else:
            sc = "{:.5f}".format(self.SC)[:7]

        if self.SS is None:
            ss = " "*7
        else:
            ss = "{:.5f}".format(self.SS)[:7]

        if (self.ST is not None) or (self.SC is not None) or (self.SS is not None):

            return f"MAT1    {self.ID}{idspaces} {e} {g} {nu} {rho} {texp} {tref} {ge}\n" + \
                   f"         {st} {sc} {ss}\n"
        else:

            return f"MAT1    {self.ID}{idspaces} {e} {g} {nu} {rho} {texp} {tref} {ge}\n"


def set_material(**kwargs: dict[str: Any]) -> MACMat | MACMatNL:
    """
    Function to set a material as MACMaterial object. The function use the kwargs dictionary. The supported type of
    materials are:
        - MATS1: set_material(id=int, type="MATS1", stressstrain=MACTable, nonlinearity="NLELAST"|"PLASTIC  ", yieldstress=float)
    """
    if kwargs["type"] == "MATS1":

        stressstrain = kwargs["stressstrain"]
        type_ = kwargs["type"]
        nonlinearity = kwargs["nonlinearity"]
        yieldstress = kwargs["yieldstress"]
        id_ = kwargs["id"]
        material = MACMatNL(id_, type_, stressstrain, nonlinearity, yieldstress)

        return material

    elif kwargs["type"] == "MAT1":

        id_ = kwargs["id"]
        type_ = kwargs["type"]
        e = kwargs["e"]
        nu = kwargs["nu"]
        g = kwargs.get("g", None)
        rho = kwargs.get("rho", None)
        texp = kwargs.get("texp", None)
        tref = kwargs.get("tref", None)
        ge = kwargs.get("ge", None)
        st = kwargs.get("st", None)
        sc = kwargs.get("sc", None)
        ss = kwargs.get("ss", None)
        material = MACMat(id_, type_, e, nu, g, rho, texp, tref, ge, st, sc, ss)

        return material

    else:
        raise ValueError("The material type is not supported by the MACMaterial class.")