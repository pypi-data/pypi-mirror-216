"""
Module with global variables for the Metamaterial Analysis Code (MAC) package.
"""
from typing import Set
from MetamaterialAnalysisCode.classes.MACElement import MACElement

global NODES_DICT
NODES_DICT = dict()

global ELEMENTS_SET
ELEMENTS_SET: Set[MACElement] = set()

MAC_VERSION = "0.0"

AUTHOR = "Manuel Sanchez Garcia"
CONTRIBUTORS = []
