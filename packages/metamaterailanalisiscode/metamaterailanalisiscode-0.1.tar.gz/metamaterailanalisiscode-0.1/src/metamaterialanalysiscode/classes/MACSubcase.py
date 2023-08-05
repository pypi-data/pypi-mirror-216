"""
Module with the MACSubcase class
"""

from MetamaterialAnalysisCode.classes.MACLoadCase import MACForce
from MetamaterialAnalysisCode.classes.MACLoadCase import MACSpc
from MetamaterialAnalysisCode.classes.MACLoadCase import MACEigrl
from MetamaterialAnalysisCode.classes.MACNonLinear import MACNLout, MACNLparmLD


class MACSubcase:
    """
    Class for the subcase.

    Attributes:
        ID: subcase ID
        Label: subcase label
        LoadCases: list of load cases of the subcase
        StatSub: linear static subcase. Some subcases(buckling) need a linear static subcase to work
    """

    def __init__(self, id_: int, label: str, load: list[MACForce | MACSpc, ...], spc: list[MACSpc, ...],
                 eigr: MACEigrl = None, stat_sub: 'MACSubcase' = None, nlaprmld: MACNLparmLD = None,
                 nlout: MACNLout = None, output: list[str] = None):
        """
        Constructor for MACSubcase class
        """
        ids = set()
        for i in load:
            ids.add(i.ID)
        if len(ids) > 1:
            raise ValueError("All the loads of a subcase must have the same ID")

        ids = set()
        for i in spc:
            ids.add(i.ID)
        if len(ids) > 1:
            raise ValueError("All the constrains of a subcase must have the same ID")

        self.ID = id_
        self.Label = label
        self.Load = load
        self.Spc = spc
        self.Eigr = eigr
        self.StatSub = stat_sub
        self.NLaprmLD = nlaprmld
        self.NLout = nlout
        self.Output = output

    def __str__(self):
        """
        Method to print a subcase. It uses the 8 characters format of Optistruct.
        """

        idspaces = " " * 8
        case = ""
        outstr = ""
        if isinstance(self.Output, list):
            for out in self.Output:
                outstr += "  " + out + "\n"

        if not self.Label.startswith("buckling") and isinstance(self.Load[0], MACForce):
            loadspaces = " " * (8 - len(str(self.Load[0].ID)))
            case += f"  LOAD = {loadspaces}{self.Load[0].ID}\n"

        elif not self.Label.startswith("buckling") and isinstance(self.Load[0], MACSpc):
            loadspaces = " " * (8 - len(str(self.Load[0].ID)))
            case += f"  LOAD = {loadspaces}{self.Load[0].ID}\n"

        loadspaces = " " * (8 - len(str(self.Spc[0].ID)))
        case += f"  SPC = {loadspaces}{self.Spc[0].ID}\n"

        # returns the subcase depending on its label -------------------------------------------------------------------
        if self.Label.startswith("linear"):
            return f"SUBCASE{idspaces}{self.ID}\n" + f"  LABEL {self.Label}\n" + case + outstr

        elif self.Label.startswith("buckling"):
            if self.StatSub is None:
                raise ValueError("Buckling subcase needs a linear static subcase")
            else:
                subspaces = " " * 8
                methodspace = " " * 8

            return f"SUBCASE{idspaces}{self.ID}\n" + f"  LABEL {self.Label}\n" + "ANALYSIS BUCK\n" + case + \
                   f"  METHOD(STRUCTURE) ={methodspace}{self.Eigr.ID}\n" + \
                   f"  STATSUB(BUCKLING) ={subspaces}{self.StatSub.ID}\n" + outstr

        elif self.Label.startswith("nonlinear"):
            return f"SUBCASE{idspaces}{self.ID}\n" + f"  LABEL {self.Label}\n" + "ANALYSIS NLSTAT\n" + case + \
                   f"  NLPARM(LGDISP) =        {self.NLaprmLD.ID}\n" + \
                   f"  NLOUT =        {self.NLout.ID}\n" + outstr


def set_subcase(id: int, label: str, constraints: list[MACSpc, ...], loads: list[MACForce | MACSpc, ...] = None,
                eigr: MACEigrl = None, stat_sub: object = None, nlparmld: MACNLparmLD = None, nlout: MACNLout = None,
                output: list[str] = None):
    """
    Function to set a subcase. It returns a MACSubcase object.

    Arguments:
        - id: subcase ID
        - label: subcase label ("linear", "buckling")
        - load_cases: list of load cases of the subcase
        - stat_sub: (opcional) linear static subcase. Some subcases (buckling) need a linear static subcase to work
    """
    if loads is None:
        loads = []

    # check if all the loads have the same ID
    ids = set()
    for i in loads:
        ids.add(i.ID)
    if len(ids) > 1:
        raise ValueError("All the loads of a subcase must have the same ID")

    # check if all the constraints have the same ID
    ids = set()
    for i in constraints:
        ids.add(i.ID)
    if len(ids) > 1:
        raise ValueError("All the constrains of a subcase must have the same ID")

    return MACSubcase(id, label, loads, constraints, eigr, stat_sub, nlparmld, nlout, output)
