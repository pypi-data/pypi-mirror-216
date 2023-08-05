"""
Module for the NonLinear Parameters for Large Displacements (NLaprmLD) class and NonLinear Output (NLout) class.
"""


class MACNLparmLD:
    """
    Class for the NonLinear Parameters for Large Displacements (NLparmLD).
    """

    def __init__(self, id: int, dt: float):
        """
        Constructor for MACNLparmLD class
        """
        self.ID = id
        self.DT = dt

    def __str__(self):
        """
        Method to print the NonLinear Parameters for Large Displacements (NLaprmLD) class.
        """
        idspaces = " " * (8 - len(str(self.ID)))
        dtspaces = " " * (8 - len(str(self.DT)))
        return f"NLPARM  {idspaces}{self.ID}        {dtspaces}{self.DT}\n"


class MACNLout:
    """
    Class for the NonLinear Output (NLout).
    """

    def __init__(self, id: int, nint: int):
        """
        Constructor for MACNLout class
        """
        self.ID = id
        self.NINT = nint

    def __str__(self):
        """
        Method to print the NonLinear Output (NLout) class.
        """
        idspaces = " " * (8 - len(str(self.ID)))
        nintspaces = " " * (8 - len(str(self.NINT)))
        return f"NLOUT   {idspaces}{self.ID}    NINT{nintspaces}{self.NINT}\n"


def set_nlparmld(id: int, dt: float):
    """
    Function to create a NonLinear Parameters for Large Displacements (NLaprmLD) class.
    """
    return MACNLparmLD(id, dt)


def set_nlout(id: int, nint: int):
    """
    Function to create a NonLinear Output (NLout) class.
    """
    return MACNLout(id, nint)