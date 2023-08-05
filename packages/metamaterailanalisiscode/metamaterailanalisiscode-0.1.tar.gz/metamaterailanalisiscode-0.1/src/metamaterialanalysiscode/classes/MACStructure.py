"""
Cell Structure module for Metamaterial Analysis Code (MAC). It represents the structure.
"""
import sys

from .MACMaterial import MACMaterial
from .MACProperty import MACProperty
from .MACNode import MACNode
from .MACElement import MACElement
from .MACGlobals import NODES_DICT, ELEMENTS_SET


class MACAuxetic:
    """
    Auxetic Structure class for Metamaterial Analysis Code (MAC). It represents the auxetic structure.

    Attributes:
        Djoint: distance between the auxiliary nodes (M1, M2) and the horizontal central plane
        Dstar: distance between the first group of nodes (B1,...,B6) and the center of the cell
        Heightstar: distance between the second group of nodes (S1,...,S6) and the horizontal central plane
    """

    def __init__(self, djoint: float, dstar: float, heightstar: float, hcapas: float,hprisma: float,
                 stepx: float, stepy: float, nelem: int):
        """
        Constructor for MACAuxetic class
        """

        self.__djoint = djoint
        self.__dstar = dstar
        self.__heightstar = heightstar
        self.__hcapas = hcapas
        self.__hprisma = hprisma
        self.__stepx = stepx
        self.__stepy = stepy
        self.Type = "Auxetic"
        self.__nelem = nelem

    @property
    def Djoint(self) -> float:
        return self.__djoint

    @property
    def Dstar(self) -> float:
        return self.__dstar

    @property
    def Heightstar(self) -> float:
        return self.__heightstar

    @property
    def Hcapas(self) -> float:
        return self.__hcapas

    @property
    def Hprisma(self) -> float:
        return self.__hprisma

    @property
    def Stepx(self) -> float:
        return self.__stepx

    @property
    def Stepy(self) -> float:
        return self.__stepy

    def build(self, cellcenter: tuple[float, ...], mat: MACMaterial, prop: MACProperty, vvector: tuple)\
            -> tuple[tuple[MACNode, ...], tuple[MACElement, ...]]:

        # M1
        x = round(cellcenter[0], 4)
        y = round(cellcenter[1], 4)
        z = round(cellcenter[2] + self.__djoint, 4)
        M1 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = M1

        # M2
        x = round(cellcenter[0], 4)
        y = round(cellcenter[1], 4)
        z = round(cellcenter[2] - self.__djoint, 4)
        M2 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = M2

        # S1
        x1 = round(cellcenter[0] + self.__stepx, 4)
        y1 = round(cellcenter[1], 4)
        z1 = round(cellcenter[2] + self.__heightstar, 4)
        S1 = NODES_DICT.get((x1, y1, z1), MACNode(len(NODES_DICT) + 1, (x1, y1, z1)))
        NODES_DICT[(x1, y1, z1)] = S1

        # S2
        x2 = round(cellcenter[0] + self.__stepx/2, 4)
        y2 = round(cellcenter[1] - (3**0.5)/2 * self.__stepy, 4)
        z2 = round(cellcenter[2] - self.__heightstar, 4)
        S2 = NODES_DICT.get((x2, y2, z2), MACNode(len(NODES_DICT) + 1, (x2, y2, z2)))
        NODES_DICT[(x2, y2, z2)] = S2

        # S3
        x3 = round(cellcenter[0] - self.__stepx/2, 4)
        y3 = round(cellcenter[1] - (3**0.5)/2 * self.__stepy, 4)
        z3 = round(cellcenter[2] + self.__heightstar, 4)
        S3 = NODES_DICT.get((x3, y3, z3), MACNode(len(NODES_DICT) + 1, (x3, y3, z3)))
        NODES_DICT[(x3, y3, z3)] = S3

        # S4
        x4 = round(cellcenter[0] - self.__stepx, 4)
        y4 = round(cellcenter[1], 4)
        z4 = round(cellcenter[2] - self.__heightstar, 4)
        S4 = NODES_DICT.get((x4, y4, z4), MACNode(len(NODES_DICT) + 1, (x4, y4, z4)))
        NODES_DICT[(x4, y4, z4)] = S4

        # S5
        x5 = round(cellcenter[0] - self.__stepx/2, 4)
        y5 = round(cellcenter[1] + (3**0.5)/2 * self.__stepy, 4)
        z5 = round(cellcenter[2] + self.__heightstar, 4)
        S5 = NODES_DICT.get((x5, y5, z5), MACNode(len(NODES_DICT) + 1, (x5, y5, z5)))
        NODES_DICT[(x5, y5, z5)] = S5

        # S6
        x6 = round(cellcenter[0] + self.__stepx/2, 4)
        y6 = round(cellcenter[1] + (3**0.5)/2 * self.__stepy, 4)
        z6 = round(cellcenter[2] - self.__heightstar, 4)
        S6 = NODES_DICT.get((x6, y6, z6), MACNode(len(NODES_DICT) + 1, (x6, y6, z6)))
        NODES_DICT[(x6, y6, z6)] = S6

        # B1
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x6+x5)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y6+y5)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z6+z5)/2, 4)
        B1 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B1

        # B2
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x1+x6)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y1+y6)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z1+z6)/2, 4)
        B2 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B2

        # B3
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x1+x2)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y1+y2)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z1+z2)/2, 4)
        B3 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B3

        # B4
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x2+x3)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y2+y3)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z2+z3)/2, 4)
        B4 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B4

        # B5
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x4+x3)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y4+y3)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z4+z3)/2, 4)
        B5 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B5

        # B6
        x = round((2 - self.__dstar)*cellcenter[0] - (1-self.__dstar)*(x4+x5)/2, 4)
        y = round((2 - self.__dstar)*cellcenter[1] - (1-self.__dstar)*(y4+y5)/2, 4)
        z = round((2 - self.__dstar)*cellcenter[2] - (1-self.__dstar)*(z4+z5)/2, 4)
        B6 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = B6

        # DN1, DN2, DN3, UP1, UP2, UP3
        x = round(cellcenter[0] + 0.5*self.__stepx, 4)
        y = round(cellcenter[1] - (3**0.5)/2 * self.__stepy, 4)
        z = round(cellcenter[2] - self.__hprisma - self.__heightstar, 4)
        DN1 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = DN1

        x = round(cellcenter[0] - self.__stepx, 4)
        y = round(cellcenter[1], 4)
        z = round(cellcenter[2] - self.__hprisma - self.__heightstar, 4)
        DN2 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = DN2

        x = round(cellcenter[0] + 0.5 * self.__stepx, 4)
        y = round(cellcenter[1] + (3**0.5) / 2 * self.__stepy, 4)
        z = round(cellcenter[2] - self.__hprisma - self.__heightstar, 4)
        DN3 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = DN3

        x = round(cellcenter[0] + self.__stepx, 4)
        y = round(cellcenter[1], 4)
        z = round(cellcenter[2] + self.__hprisma + self.__heightstar, 4)
        UP1 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = UP1

        x = round(cellcenter[0] - 0.5 * self.__stepx, 4)
        y = round(cellcenter[1] - (3**0.5) / 2 * self.__stepy, 4)
        z = round(cellcenter[2] + self.__hprisma + self.__heightstar, 4)
        UP2 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = UP2

        x = round(cellcenter[0] - 0.5 * self.__stepx, 4)
        y = round(cellcenter[1] + (3**0.5) / 2 * self.__stepy, 4)
        z = round(cellcenter[2] + self.__hprisma + self.__heightstar, 4)
        UP3 = NODES_DICT.get((x, y, z), MACNode(len(NODES_DICT) + 1, (x, y, z)))
        NODES_DICT[(x, y, z)] = UP3

        if self.__nelem == 1:

            nodes = (M1, M2, B1, B2, B3, B4, B5, B6, S1, S2, S3, S4, S5, S6, DN1, DN2, DN3, UP1, UP2, UP3)

            if M1.Coords == M2.Coords:
                sys.exit("M1 es coincidente con M2 porque v1 = 0. Usar el metodo de 4 vigas")

            # CBEAMS that connect the nodes and build the cell
            elemcount = len(ELEMENTS_SET)

            # M1_B1, M1_B2, M1_B3, M1_B4, M1_B5, M1_B6
            M1_B1 = MACElement(elemcount + 1, "CBEAM", [M1, B1], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B1)

            M1_B2 = MACElement(elemcount + 2, "CBEAM", [M1, B2], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B2)

            M1_B3 = MACElement(elemcount + 3, "CBEAM", [M1, B3], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B3)

            M1_B4 = MACElement(elemcount + 4, "CBEAM", [M1, B4], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B4)

            M1_B5 = MACElement(elemcount + 5, "CBEAM", [M1, B5], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B5)

            M1_B6 = MACElement(elemcount + 6, "CBEAM", [M1, B6], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_B6)

            # M2_B1, M2_B2, M2_B3, M2_B4, M2_B5, M2_B6
            M2_B1 = MACElement(elemcount + 7, "CBEAM", [M2, B1], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B1)

            M2_B2 = MACElement(elemcount + 8, "CBEAM", [M2, B2], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B2)

            M2_B3 = MACElement(elemcount + 9, "CBEAM", [M2, B3], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B3)

            M2_B4 = MACElement(elemcount + 10, "CBEAM", [M2, B4], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B4)

            M2_B5 = MACElement(elemcount + 11, "CBEAM", [M2, B5], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B5)

            M2_B6 = MACElement(elemcount + 12, "CBEAM", [M2, B6], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_B6)

            # S1_B6, B6_S2, S2_B1, B1_S3, S3_B2, B2_S4, S4_B3, B3_S5, S5_B4, B4_S6, S6_B5, B5_S1
            S1_B6 = MACElement(elemcount + 13, "CBEAM", [S1, B6], [mat], [prop], vvector)
            ELEMENTS_SET.add(S1_B6)

            B6_S2 = MACElement(elemcount + 14, "CBEAM", [B6, S2], [mat], [prop], vvector)
            ELEMENTS_SET.add(B6_S2)

            S2_B1 = MACElement(elemcount + 15, "CBEAM", [S2, B1], [mat], [prop], vvector)
            ELEMENTS_SET.add(S2_B1)

            B1_S3 = MACElement(elemcount + 16, "CBEAM", [B1, S3], [mat], [prop], vvector)
            ELEMENTS_SET.add(B1_S3)

            S3_B2 = MACElement(elemcount + 17, "CBEAM", [S3, B2], [mat], [prop], vvector)
            ELEMENTS_SET.add(S3_B2)

            B2_S4 = MACElement(elemcount + 18, "CBEAM", [B2, S4], [mat], [prop], vvector)
            ELEMENTS_SET.add(B2_S4)

            S4_B3 = MACElement(elemcount + 19, "CBEAM", [S4, B3], [mat], [prop], vvector)
            ELEMENTS_SET.add(S4_B3)

            B3_S5 = MACElement(elemcount + 20, "CBEAM", [B3, S5], [mat], [prop], vvector)
            ELEMENTS_SET.add(B3_S5)

            S5_B4 = MACElement(elemcount + 21, "CBEAM", [S5, B4], [mat], [prop], vvector)
            ELEMENTS_SET.add(S5_B4)

            B4_S6 = MACElement(elemcount + 22, "CBEAM", [B4, S6], [mat], [prop], vvector)
            ELEMENTS_SET.add(B4_S6)

            S6_B5 = MACElement(elemcount + 23, "CBEAM", [S6, B5], [mat], [prop], vvector)
            ELEMENTS_SET.add(S6_B5)

            B5_S1 = MACElement(elemcount + 24, "CBEAM", [B5, S1], [mat], [prop], vvector)
            ELEMENTS_SET.add(B5_S1)

            # M1_S1, M1_S3, M1_S5, M2_S2, M2_S4, M2_S6
            M1_S1 = MACElement(elemcount + 25, "CBEAM", [M1, S1], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_S1)

            M1_S3 = MACElement(elemcount + 26, "CBEAM", [M1, S3], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_S3)

            M1_S5 = MACElement(elemcount + 27, "CBEAM", [M1, S5], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_S5)

            M2_S2 = MACElement(elemcount + 28, "CBEAM", [M2, S2], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_S2)

            M2_S4 = MACElement(elemcount + 29, "CBEAM", [M2, S4], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_S4)

            M2_S6 = MACElement(elemcount + 30, "CBEAM", [M2, S6], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_S6)

            # M1_UP1, M1_UP2, M1_UP3, M2_DN1, M2_DN2, M2_DN3
            M1_UP1 = MACElement(elemcount + 31, "CBEAM", [M1, UP1], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_UP1)

            M1_UP2 = MACElement(elemcount + 32, "CBEAM", [M1, UP2], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_UP2)

            M1_UP3 = MACElement(elemcount + 33, "CBEAM", [M1, UP3], [mat], [prop], vvector)
            ELEMENTS_SET.add(M1_UP3)

            M2_DN1 = MACElement(elemcount + 34, "CBEAM", [M2, DN1], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_DN1)

            M2_DN2 = MACElement(elemcount + 35, "CBEAM", [M2, DN2], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_DN2)

            M2_DN3 = MACElement(elemcount + 36, "CBEAM", [M2, DN3], [mat], [prop], vvector)
            ELEMENTS_SET.add(M2_DN3)

            # All elements in a tuple
            elements = (M1_B1, M1_B2, M1_B3, M1_B4, M1_B5, M1_B6, M2_B1, M2_B2, M2_B3, M2_B4, M2_B5, M2_B6, S1_B6, B6_S2,
                        S2_B1, B1_S3, S3_B2, B2_S4, S4_B3, B3_S5, S5_B4, B4_S6, S6_B5, B5_S1, M1_S1, M1_S3, M1_S5, M2_S2,
                        M2_S4, M2_S6, M1_UP1, M1_UP2, M1_UP3, M2_DN1, M2_DN2, M2_DN3)

        elif self.__nelem == 4:
            internodes = list()
            elements = list()
            elemcount = len(ELEMENTS_SET)

            # M1_B1 intermediate nodes
            for coord in _gen3p(M1.Coords, B1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B1], [mat], [prop], vvector))

            # M1_B2 intermediate nodes
            for coord in _gen3p(M1.Coords, B2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B2], [mat], [prop], vvector))

            # M1_B3 intermediate nodes
            for coord in _gen3p(M1.Coords, B3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B3], [mat], [prop], vvector))

            # M1_B4 intermediate nodes
            for coord in _gen3p(M1.Coords, B4.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B4], [mat], [prop], vvector))

            # M1_B5 intermediate nodes
            for coord in _gen3p(M1.Coords, B5.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B5], [mat], [prop], vvector))

            # M1_B6 intermediate nodes
            for coord in _gen3p(M1.Coords, B6.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B6], [mat], [prop], vvector))

            # Esto se añade porque M1 coincide con M2 si v1 = 0
            if M1.Coords != M2.Coords:

                # M2_B1 intermediate nodes
                for coord in _gen3p(M2.Coords, B1.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B1], [mat], [prop], vvector))

                # M2_B2 intermediate nodes
                for coord in _gen3p(M2.Coords, B2.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B2], [mat], [prop], vvector))

                # M2_B3 intermediate nodes
                for coord in _gen3p(M2.Coords, B3.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B3], [mat], [prop], vvector))

                # M2_B4 intermediate nodes
                for coord in _gen3p(M2.Coords, B4.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B4], [mat], [prop], vvector))

                # M2_B5 intermediate nodes
                for coord in _gen3p(M2.Coords, B5.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B5], [mat], [prop], vvector))

                # M2_B6 intermediate nodes
                for coord in _gen3p(M2.Coords, B6.Coords):
                    internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                    NODES_DICT[coord] = internodes[-1]
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [M2, internodes[-3]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-3], internodes[-2]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-2], internodes[-1]], [mat], [prop], vvector))
                elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                           [internodes[-1], B6], [mat], [prop], vvector))

            # S1_B6 intermediate nodes
            for coord in _gen3p(S1.Coords, B6.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B6], [mat], [prop], vvector))

            # B6_S2 intermediate nodes
            for coord in _gen3p(B6.Coords, S2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B6, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S2], [mat], [prop], vvector))

            # S2_B1 intermediate nodes
            for coord in _gen3p(S2.Coords, B1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S2, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B1], [mat], [prop], vvector))

            # B1_S3 intermediate nodes
            for coord in _gen3p(B1.Coords, S3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S3], [mat], [prop], vvector))

            # S3_B2 intermediate nodes
            for coord in _gen3p(S3.Coords, B2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S3, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B2], [mat], [prop], vvector))

            # B2_S4 intermediate nodes
            for coord in _gen3p(B2.Coords, S4.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B2, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S4], [mat], [prop], vvector))

            # S4_B3 intermediate nodes
            for coord in _gen3p(S4.Coords, B3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S4, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B3], [mat], [prop], vvector))

            # B3_S5 intermediate nodes
            for coord in _gen3p(B3.Coords, S5.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B3, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S5], [mat], [prop], vvector))

            # S5_B4 intermediate nodes
            for coord in _gen3p(S5.Coords, B4.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S5, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B4], [mat], [prop], vvector))

            # B4_S6 intermediate nodes
            for coord in _gen3p(B4.Coords, S6.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B4, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S6], [mat], [prop], vvector))

            # S6_B5 intermediate nodes
            for coord in _gen3p(S6.Coords, B5.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [S6, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], B5], [mat], [prop], vvector))

            # B5_S1 intermediate nodes
            for coord in _gen3p(B5.Coords, S1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [B5, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S1], [mat], [prop], vvector))

            # M1_S1 intermediate nodes
            for coord in _gen3p(M1.Coords, S1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S1], [mat], [prop], vvector))

            # M1_S3 intermediate nodes
            for coord in _gen3p(M1.Coords, S3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S3], [mat], [prop], vvector))

            # M1_S5 intermediate nodes
            for coord in _gen3p(M1.Coords, S5.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S5], [mat], [prop], vvector))

            # M2_S2 intermediate nodes
            for coord in _gen3p(M2.Coords, S2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M2, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S2], [mat], [prop], vvector))

            # M2_S4 intermediate nodes
            for coord in _gen3p(M2.Coords, S4.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M2, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S4], [mat], [prop], vvector))

            # M2_S6 intermediate nodes
            for coord in _gen3p(M2.Coords, S6.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M2, internodes[-3]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], S6], [mat], [prop], vvector))

            # M1_UP1 intermediate nodes
            for coord in _gen3p(M1.Coords, UP1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], UP1], [mat], [prop], vvector, aux=True))

            # M1_UP2 intermediate nodes
            for coord in _gen3p(M1.Coords, UP2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], UP2], [mat], [prop], vvector, aux=True))

            # M1_UP3 intermediate nodes
            for coord in _gen3p(M1.Coords, UP3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M1, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], UP3], [mat], [prop], vvector, aux=True))

            # M2_DN1 intermediate nodes
            for coord in _gen3p(M2.Coords, DN1.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M2, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [internodes[-1], DN1], [mat], [prop], vvector, aux=True))

            # M2_DN2 intermediate nodes
            for coord in _gen3p(M2.Coords, DN2.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                       [M2, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-1], DN2], [mat], [prop], vvector, aux=True))

            # M2_DN3 intermediate nodes
            for coord in _gen3p(M2.Coords, DN3.Coords):
                internodes.append(MACNode(len(NODES_DICT) + 1, coord))
                NODES_DICT[coord] = internodes[-1]
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [M2, internodes[-3]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-3], internodes[-2]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-2], internodes[-1]], [mat], [prop], vvector, aux=True))
            elements.append(MACElement(elemcount + len(elements) + 1, "CBEAM",
                                        [internodes[-1], DN3], [mat], [prop], vvector, aux=True))

            for element in elements:
                ELEMENTS_SET.add(element)

            elements = tuple(elements)
            nodes = tuple([M1, M2, B1, B2, B3, B4, B5, B6, S1, S2, S3, S4, S5, S6, DN1, DN2, DN3, UP1, UP2, UP3]
                          + internodes)


        return nodes, elements


def _gen3p(point1: tuple, point2: tuple) -> tuple:
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    # Calculate the intermediate points
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2
    z_mid = (z1 + z2) / 2

    x_quarter = (3 * x1 + x2) / 4
    y_quarter = (3 * y1 + y2) / 4
    z_quarter = (3 * z1 + z2) / 4

    x_three_quarters = (x1 + 3 * x2) / 4
    y_three_quarters = (y1 + 3 * y2) / 4
    z_three_quarters = (z1 + 3 * z2) / 4

    # Create and return the three points between
    point_mid = (x_mid, y_mid, z_mid)
    point_quarter = (x_quarter, y_quarter, z_quarter)
    point_three_quarters = (x_three_quarters, y_three_quarters, z_three_quarters)

    return point_quarter, point_mid, point_three_quarters



def set_structure(**kwargs) -> MACAuxetic:
    """ Function to set the structure of the cell. It uses **kwargs, a dictionary of parameters. Depending on the
    type of the structure an object of the corresponding class is created and returned. Types supported are:
        - Auxetic: set_structure(type="Auxetic", djoint=float, dstar=float, heightstar=float, hcapas=float,+
                                 hprisma=float, stepx=0.1, stepy=0.1, nelem=1)
    """
    if kwargs["type"] == "Auxetic":

        structure = MACAuxetic(djoint=kwargs["djoint"], dstar=kwargs["dstar"], heightstar=kwargs["heightstar"],
                               hcapas=kwargs["hcapas"], hprisma=kwargs["hprisma"], stepx=kwargs["stepx"],
                               stepy=kwargs["stepy"], nelem=kwargs["nelem"])

        return structure
