import sys
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


class BondDirection(Enum):
    VERTICAL = "|"
    UL_LR = "\\"
    LL_UR = "/"


class BondAlreadyOccupiedError(ValueError):
    pass


@dataclass
class Atom:
    element: Element
    bonds: list["Bond"] = None

    def __post_init__(self):
        if self.bonds is None:
            self.bonds = []

    def bonded_atoms(self) -> Iterable[tuple["Atom", BondDirection, int]]:
        for bond in self.bonds:
            other_atom = [a for a in bond.atoms if a is not self][0]
            yield other_atom, bond.direction, bond.number


@dataclass
class Bond:
    atoms: tuple[Atom, Atom]
    direction: BondDirection
    number: int = 1

    def __post_init__(self):
        for atom in self.atoms:
            if any(b.direction is self.direction for b in atom.bonds):
                raise BondAlreadyOccupiedError
            atom.bonds.append(self)


PADDING = 50
ATOM_RADIUS = 20
BOND_THICKNESS = 6
BOND_COLOR = "#ffffff"
BOND_LENGTH = 100
BOND_SPACING = 16
ROOT3OVER2 = (3**.5)/2


NEIGHBOR_LOCATIONS: dict[BondDirection, tuple[int, int, int]] = {
    BondDirection.VERTICAL: (0, 0, -BOND_LENGTH),
    BondDirection.UL_LR: (120, round(BOND_LENGTH*ROOT3OVER2), BOND_LENGTH//2),
    BondDirection.LL_UR: (60, -round(BOND_LENGTH*ROOT3OVER2), BOND_LENGTH//2),
}


def molecule_svg(leftmost_atom: Atom, height: int, starting_height: int):
    paths = []

    drawn_atoms: set[int] = set()
    atoms_to_draw: list[tuple[Atom, [int, int], bool]] = [
        (leftmost_atom, (PADDING, starting_height), True),
    ]

    rightmost: int = 0

    while atoms_to_draw:
        (drawing_atom, (x, y), top_vertical), atoms_to_draw = atoms_to_draw[0], atoms_to_draw[1:]
        for other_atom, direction, number in drawing_atom.bonded_atoms():
            if id(other_atom) in drawn_atoms:
                continue

            degrees, dx, dy = NEIGHBOR_LOCATIONS[direction]
            if not top_vertical:
                dx, dy = -dx, -dy

            atoms_to_draw.append((other_atom, (x+dx, y+dy), not top_vertical))

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
                    rotation=Rotation(degrees, bond_cx, bond_cy)
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
        background_color="black"
    )


HORIZONTAL_FLIP = {
    BondDirection.VERTICAL: BondDirection.VERTICAL,
    BondDirection.UL_LR: BondDirection.LL_UR,
    BondDirection.LL_UR: BondDirection.UL_LR,
}


def flip_molecule_horizontally(starting_atom: Atom):
    atom_stack = [starting_atom]
    seen_bond_ids = set()

    while atom_stack:
        curr_atom, atom_stack = atom_stack[0], atom_stack[1:]
        for bond in curr_atom.bonds:
            if id(bond) in seen_bond_ids:
                continue

            atom_stack += bond.atoms # this will readd curr_atom, but its bonds will get skipped

            bond.direction = HORIZONTAL_FLIP[bond.direction]

            seen_bond_ids.add(id(bond))


def phenyl():
    """Returns a list of six carbons in a phenyl ring, in clockwise order with the 0th carbon being the top one"""

    direction_order = [BondDirection.UL_LR, BondDirection.VERTICAL, BondDirection.LL_UR]

    carbons = [Atom(Element.CARBON) for _ in range(6)]
    for i in range(6):
        Bond((carbons[i], carbons[(i+1)%6]), direction_order[i%3], (i%2) + 1)

    return carbons


def alanine():
    return Atom(Element.CARBON)


def cysteine():
    C = Atom(Element.CARBON)
    Bond((C, Atom(Element.SULFUR)), BondDirection.UL_LR)
    return C


def glutamic_acid():
    carbons = [Atom(Element.CARBON) for _ in range(3)]
    Bond((carbons[0], carbons[1]), BondDirection.UL_LR)
    Bond((carbons[1], carbons[2]), BondDirection.VERTICAL)
    Bond((carbons[2], Atom(Element.OXYGEN)), BondDirection.UL_LR, 2)
    Bond((carbons[2], Atom(Element.OXYGEN)), BondDirection.LL_UR)
    return carbons[0]


def glycine():
    return None


def isoleucine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    Bond((carbons[0], carbons[1]), BondDirection.LL_UR)
    Bond((carbons[0], carbons[2]), BondDirection.UL_LR)
    Bond((carbons[2], carbons[3]), BondDirection.VERTICAL)
    return carbons[0]


def leucine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    Bond((carbons[0], carbons[1]), BondDirection.UL_LR)
    Bond((carbons[1], carbons[2]), BondDirection.VERTICAL)
    Bond((carbons[1], carbons[3]), BondDirection.LL_UR)
    return carbons[0]


def asparigine():
    C1 = Atom(Element.CARBON)
    C2 = Atom(Element.CARBON)
    Bond((C1, C2), BondDirection.UL_LR)
    Bond((C2, Atom(Element.OXYGEN)), BondDirection.LL_UR, 2)
    Bond((C2, Atom(Element.NITROGEN)), BondDirection.VERTICAL)
    return C1


def pyrrolycine():
    carbons = [Atom(Element.CARBON) for _ in range(4)]
    for i in range(3):
        Bond((carbons[i], carbons[i+1]), BondDirection.VERTICAL if i%2 else BondDirection.UL_LR)
    N = Atom(Element.NITROGEN)
    Bond((carbons[-1], N), BondDirection.VERTICAL)

    more_carbons = [Atom(Element.CARBON) for _ in range(5)]
    Bond((N, more_carbons[0]), BondDirection.UL_LR)
    Bond((more_carbons[0], Atom(Element.OXYGEN)), BondDirection.LL_UR, 2)
    Bond((more_carbons[0], more_carbons[1]), BondDirection.VERTICAL)

    # TODO figure out 5-membered rings

    return carbons[0]


def selenocysteine():
    C = Atom(Element.CARBON)
    Bond((C, Atom(Element.SELENIUM)), BondDirection.UL_LR)
    return C


def tyrosine():
    C = Atom(Element.CARBON)
    PH = phenyl()
    Bond((C, PH[5]), BondDirection.UL_LR)
    Bond((PH[2], Atom(Element.OXYGEN)), BondDirection.UL_LR)
    return C


AMINO_ACIDS = {
    "A": alanine,
    "C": cysteine,
    "E": glutamic_acid,
    "G": glycine,
    "I": isoleucine,
    "L": leucine,
    "N": asparigine,
    # "O": pyrrolycine,
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
        Bond((N, middleC), BondDirection.UL_LR, 1)
        rightC = Atom(Element.CARBON)
        Bond((middleC, rightC), BondDirection.LL_UR, 1)
        doubleBondedO = Atom(Element.OXYGEN)
        Bond((rightC, doubleBondedO), BondDirection.VERTICAL, 2)

        side_chain = AMINO_ACIDS[letter]()
        if side_chain is not None:
            Bond((middleC, side_chain), BondDirection.VERTICAL)

        return cls(N, rightC)


if __name__ == "__main__":
    letters = sys.argv[1]

    curr_amino = AminoAcid.from_letter_code(letters[0])
    leftmost_atom = curr_amino.N

    peptide_bond_direction = BondDirection.UL_LR

    for letter in letters[1:]:
        next_amino = AminoAcid.from_letter_code(letter)

        if peptide_bond_direction is BondDirection.UL_LR:
            flip_molecule_horizontally(next_amino.N)

        Bond((curr_amino.C, next_amino.N), peptide_bond_direction)
        peptide_bond_direction = HORIZONTAL_FLIP[peptide_bond_direction]

        curr_amino = next_amino

    Bond((curr_amino.C, Atom(Element.OXYGEN)), peptide_bond_direction)

    image_height = 1400
    with open(f"images/{letters}.svg", "w") as fh:
        fh.write(molecule_svg(leftmost_atom, height=image_height, starting_height=image_height//2))
