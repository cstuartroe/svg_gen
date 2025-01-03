import os
import sys
import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from utils import svg_template, circle_template, rectangle_template, Rotation


class Element(Enum):
    CARBON = "#000000"
    NITROGEN = "#0077ff"
    OXYGEN = "#ff0000"
    SULFUR = "#ffff00"

    # Selenium is orange according to JMOL
    # https://en.wikipedia.org/wiki/CPK_coloring#Modern_variants
    SELENIUM = "#ffa100"


class BondAlreadyOccupiedError(ValueError):
    pass


@dataclass
class Atom:
    element: Element
    bonds: list["Bond"] = None

    def __post_init__(self):
        if self.bonds is None:
            self.bonds = []

    def bonded_atoms(self) -> Iterable[tuple["Atom", int, int]]:
        for bond in self.bonds:
            other_atom = [a for a in bond.atoms if a is not self][0]
            if bond.atoms[0] is self:
                angle = bond.angle
            else:
                angle = (bond.angle + 180) % 360
            yield other_atom, angle, bond.number


@dataclass
class Bond:
    atoms: tuple[Atom, Atom]
    # angle is in degrees, starting at the top and going clockwise
    # it is from the first atom to the second
    angle: int
    number: int = 1

    def __post_init__(self):
        for atom in self.atoms:
            if any(angle == self.angle for _, angle, _ in atom.bonded_atoms()):
                raise BondAlreadyOccupiedError
            atom.bonds.append(self)


PADDING = 50
ATOM_RADIUS = 20
BOND_THICKNESS = 6
BOND_LENGTH = 100
BOND_SPACING = 16
ROOT3OVER2 = (3**.5)/2

BOND_COLOR = "#ffffff"
BACKGROUND_COLOR = "black"


def molecule_svg(leftmost_atom: Atom, height: int, starting_height: int):
    paths = []

    drawn_atoms: set[int] = set()
    atoms_to_draw: list[tuple[Atom, [int, int]]] = [
        (leftmost_atom, (PADDING, starting_height)),
    ]

    rightmost: int = 0

    while atoms_to_draw:
        (drawing_atom, (x, y)), atoms_to_draw = atoms_to_draw[0], atoms_to_draw[1:]
        for other_atom, angle, number in drawing_atom.bonded_atoms():
            if id(other_atom) in drawn_atoms:
                continue

            # it seems backwards because I'm starting at the top and
            # going clockwise
            dx = round(math.sin(angle*math.pi/180)*BOND_LENGTH)
            dy = -round(math.cos(angle*math.pi/180)*BOND_LENGTH)

            atoms_to_draw.append((other_atom, (x+dx, y+dy)))

            bond_cx = x + dx//2
            bond_cy = y + dy//2

            for bond_i in range(number):
                bond_x = bond_cx - BOND_THICKNESS//2 - BOND_SPACING*(number-1)//2 + bond_i*BOND_SPACING
                bond_y = bond_cy - BOND_LENGTH//2

                paths.append(rectangle_template(
                    x=bond_x,
                    y=bond_y,
                    width=BOND_THICKNESS,
                    height=BOND_LENGTH,
                    color=BOND_COLOR,
                    rotation=Rotation(angle % 180, bond_cx, bond_cy)
                ))

        paths.append(
            circle_template(x, y, ATOM_RADIUS + BOND_THICKNESS, BOND_COLOR)
        )
        paths.append(
            circle_template(x, y, ATOM_RADIUS, drawing_atom.element.value)
        )

        drawn_atoms.add(id(drawing_atom))
        rightmost = max(x, rightmost)

    return svg_template(
        rightmost + PADDING,
        height,
        paths,
        background_color=BACKGROUND_COLOR
    )


def flip_molecule_vertically(starting_atom: Atom):
    atom_stack = [starting_atom]
    seen_bond_ids = set()

    while atom_stack:
        curr_atom, atom_stack = atom_stack[0], atom_stack[1:]
        for bond in curr_atom.bonds:
            if id(bond) in seen_bond_ids:
                continue

            atom_stack += bond.atoms # this will readd curr_atom, but its bonds will get skipped

            bond.angle = (180 - bond.angle) % 360

            seen_bond_ids.add(id(bond))


def phenyl():
    """Returns a list of six carbons in a phenyl ring, in clockwise order with the 0th carbon being the top one"""

    carbons = [Atom(Element.CARBON) for _ in range(6)]
    for i in range(6):
        Bond((carbons[i], carbons[(i+1)%6]), ((i*60) + 120) % 360, (i%2) + 1)

    return carbons


def alanine():
    return Atom(Element.CARBON)


def cysteine():
    C = Atom(Element.CARBON)
    Bond((C, Atom(Element.SULFUR)), 120)
    return C


def glutamic_acid():
    carbons = [Atom(Element.CARBON) for _ in range(3)]
    Bond((carbons[0], carbons[1]), 120)
    Bond((carbons[1], carbons[2]), 180)
    Bond((carbons[2], Atom(Element.OXYGEN)), 120, 2)
    Bond((carbons[2], Atom(Element.OXYGEN)), 240)
    return carbons[0]


def glycine():
    return None


def isoleucine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    Bond((carbons[0], carbons[1]), 240)
    Bond((carbons[0], carbons[2]), 120)
    Bond((carbons[2], carbons[3]), 180)
    return carbons[0]


def lysine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    Bond((carbons[0], carbons[1]), 120)
    Bond((carbons[1], carbons[2]), 180)
    Bond((carbons[2], carbons[3]), 120)
    Bond((carbons[3], Atom(Element.NITROGEN)), 180)
    return carbons[0]


def leucine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    Bond((carbons[0], carbons[1]), 120)
    Bond((carbons[1], carbons[2]), 180)
    Bond((carbons[1], carbons[3]), 60)
    return carbons[0]


def asparigine():
    C1 = Atom(Element.CARBON)
    C2 = Atom(Element.CARBON)
    Bond((C1, C2), 120)
    Bond((C2, Atom(Element.OXYGEN)), 60, 2)
    Bond((C2, Atom(Element.NITROGEN)), 180)
    return C1


def pyrrolycine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    for i in range(3):
        Bond((carbons[i], carbons[i+1]), 180 if i%2 else 120)
    N = Atom(Element.NITROGEN)
    Bond((carbons[-1], N), 180)

    more_carbons = [Atom(Element.CARBON) for _ in range(5)]
    Bond((N, more_carbons[0]), 120)
    Bond((more_carbons[0], Atom(Element.OXYGEN)), 60, 2)
    Bond((more_carbons[0], more_carbons[1]), 180)
    Bond((more_carbons[1], more_carbons[2]), 180 - 54)
    Bond((more_carbons[2], more_carbons[3]), 180 + 18)
    Bond((more_carbons[3], more_carbons[4]), 270)

    N2 = Atom(Element.NITROGEN)
    Bond((more_carbons[4], N2), 360 - 18, 2)
    Bond((N2, more_carbons[1]), 54)

    return carbons[0]


def phenylalanine():
    C = Atom(Element.CARBON)
    PH = phenyl()
    Bond((C, PH[5]), 120)
    return C


def arginine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    nitrogens = [Atom(Element.NITROGEN) for _ in range(3)]
    Bond((carbons[0], carbons[1]), 120)
    Bond((carbons[1], carbons[2]), 180)
    Bond((carbons[2], nitrogens[0]), 120)
    Bond((nitrogens[0], carbons[3]), 180)
    Bond((carbons[3], nitrogens[1]), 120, 2)
    Bond((carbons[3], nitrogens[2]), 240)
    return carbons[0]


def selenocysteine():
    C = Atom(Element.CARBON)
    Bond((C, Atom(Element.SELENIUM)), 120)
    return C


def tyrosine():
    C = Atom(Element.CARBON)
    PH = phenyl()
    Bond((C, PH[5]), 120)
    Bond((PH[2], Atom(Element.OXYGEN)), 120)
    return C


AMINO_ACIDS = {
    "A": alanine,
    "C": cysteine,
    "E": glutamic_acid,
    "F": phenylalanine,
    "G": glycine,
    "I": isoleucine,
    "K": lysine,
    "L": leucine,
    "N": asparigine,
    "O": pyrrolycine,
    "R": arginine,
    "U": selenocysteine,
    "Y": tyrosine,
}


@dataclass
class AminoAcid:
    N: Atom
    C: Atom

    @classmethod
    def from_letter_code(cls, letter: str) -> "AminoAcid":
        N = Atom(Element.NITROGEN)
        middleC = Atom(Element.CARBON)
        Bond((N, middleC), 120, 1)
        rightC = Atom(Element.CARBON)
        Bond((middleC, rightC), 60, 1)
        doubleBondedO = Atom(Element.OXYGEN)
        Bond((rightC, doubleBondedO), 0, 2)

        side_chain = AMINO_ACIDS[letter]()
        if side_chain is not None:
            Bond((middleC, side_chain), 180)

        return cls(N, rightC)


def generate_peptide(letters: str):
    os.makedirs("images/peptides", exist_ok=True)
    curr_amino = AminoAcid.from_letter_code(letters[0])
    leftmost_atom = curr_amino.N

    peptide_bond_direction = 120

    for letter in letters[1:]:
        next_amino = AminoAcid.from_letter_code(letter)

        if peptide_bond_direction == 120:
            flip_molecule_vertically(next_amino.N)

        Bond((curr_amino.C, next_amino.N), peptide_bond_direction)
        peptide_bond_direction = -peptide_bond_direction % 180

        curr_amino = next_amino

    Bond((curr_amino.C, Atom(Element.OXYGEN)), peptide_bond_direction)

    image_height = 1600
    with open(f"images/peptides/{letters}.svg", "w") as fh:
        fh.write(molecule_svg(leftmost_atom, height=image_height, starting_height=image_height // 2))


if __name__ == "__main__":
    for word in (
        "ALIA",
        "CONOR",
        "CONLANG",
        "LANGUAGE",
        "NYC",
    ):
        generate_peptide(word)