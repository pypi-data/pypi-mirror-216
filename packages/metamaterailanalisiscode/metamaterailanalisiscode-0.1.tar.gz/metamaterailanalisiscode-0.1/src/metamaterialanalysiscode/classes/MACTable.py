"""
Module for the MACTable class. It represents a tables that optistruct uses for different purposes. For example, define
the strain-stress curve of a material.
"""


class MACTable:
    """
    MACTable class. It represents a tables that optistruct uses for different purposes. For example, define the
    strain-stress curve of a material.
    """

    def __init__(self, id_: int, data: list):
        """
        Constructor for MACTable class
        """
        self.ID = id_
        self.Data = data


def set_table(id: int, data: list) -> MACTable:
    """
    Function to create a MACTable object.
    """
    table = MACTable(id, data)
    return table
