"""Implements Dominion cards as a pydantic model."""

import enum
import json
import pathlib
import typing

import pydantic


class Type(str, enum.Enum):
    """The types of cards in Dominion."""

    Victory = "Victory"
    Treasure = "Treasure"
    Action = "Action"
    Attack = "Attack"
    Reaction = "Reaction"
    Curse = "Curse"


class Expansion(str, enum.Enum):
    """The expansions of Dominion."""

    Common = "Common"
    Base = "Base"

    def list_names(self) -> list[str]:
        """Return all the cards in the expansion."""
        match self:
            case Expansion.Common:
                return [
                    "Copper",
                    "Curse",
                    "Duchy",
                    "Estate",
                    "Gold",
                    "Province",
                    "Silver",
                ]
            case Expansion.Base:
                return [
                    "Artisan",
                    "Bandit",
                    "Bureaucrat",
                    "Cellar",
                    "Chapel",
                    "Council Room",
                    "Festival",
                    "Gardens",
                    "Harbinger",
                    "Library",
                    "Market",
                    "Merchant",
                    "Militia",
                    "Mine",
                    "Moat",
                    "Moneylender",
                    "Poacher",
                    "Remodel",
                    "Sentry",
                    "Smithy",
                    "Throne Room",
                    "Vassal",
                    "Village",
                    "Witch",
                    "Workshop",
                ]


class Card(pydantic.BaseModel):
    """A pydantic model for a card in Dominion.

    Attributes:
        name: The name of the card.
        cost: The cost of the card.
        types: The types of the card.
        description: The description of the card.
        expansion: The expansion of the card.
    """

    name: str
    cost: int
    types: list[Type]
    description: str
    expansion: Expansion

    def __str__(self) -> str:
        """Return the name of the card."""
        return self.name

    def __repr__(self) -> str:
        """Return a string representation of the card."""
        line = ", ".join(
            [
                f"name: {self.name}",
                f"cost: {self.cost}",
                f"types: [{', '.join(self.types)}]",
                f"description: {self.description}",
                f"expansion: {self.expansion.value}",
            ],
        )
        return f"Card({line})"

    def __eq__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Return whether the cards are identical.

        Args:
            other: The other card.

        Returns:
            Whether the cards are identical.
        """
        return self.name == other.name

    def __lt__(self, other: typing.Self) -> bool:  # type: ignore[override]
        """Allows to sort cards by their name."""
        return self.name < other.name

    def __hash__(self) -> int:
        """Return the hash of the card."""
        return hash(self.name)

    def save(self, dir_path: pathlib.Path) -> None:
        """Save the card to a json file."""
        with dir_path.joinpath(f"{self.name}.json").open("w") as f:
            json.dump(self.dict(), f, indent=2)


def load(name: str, expansion: Expansion | None = None) -> Card:
    """Load a card from a json file.

    Args:
        name: The name of the card.
        expansion: The expansion of the card.

    Returns:
        The card.

    Raises:
        FileNotFoundError: If the card does not exist.
    """
    if expansion is None:
        for e in Expansion:
            try:
                return load(name, e)
            except FileNotFoundError:
                pass

        msg = f"{name} is not a card in any expansion"
        raise FileNotFoundError(msg)

    path = pathlib.Path(__file__).parent.joinpath(
        "expansions",
        expansion.value,
        f"{name}.json",
    )
    if path.exists():
        with path.open() as f:
            return Card(**json.load(f))

    msg = f"{name} is not a card in {expansion}"
    raise FileNotFoundError(msg)


def load_expansion(expansion: Expansion) -> list[Card]:
    """Return all the kingdom cards in the given expansion."""
    expansion_dir = pathlib.Path(__file__).parent.joinpath(
        "expansions",
        expansion.value,
    )

    cards = []
    for path in filter(lambda p: p.suffix == ".json", expansion_dir.iterdir()):
        with path.open() as f:
            cards.append(Card(**json.load(f)))

    return cards


def load_base() -> list[Card]:
    """Return all the kingdom cards in the base game."""
    return load_expansion(Expansion.Base)


def load_common() -> list[Card]:
    """Return all the common cards from the base game.

    Common refers to Curses, Treasures, and non-kingdom
    Victory cards from the base game.
    """
    common_dir = pathlib.Path(__file__).parent.joinpath(
        "expansions",
        "Common",
    )

    cards = []
    for path in filter(lambda p: p.suffix == ".json", common_dir.iterdir()):
        with path.open() as f:
            cards.append(Card(**json.load(f)))

    return cards


def load_all() -> list[Card]:
    """Return all the cards in the game.

    So far, this includes all the cards in the base game and all the
    common cards from the base game.
    """
    return load_base() + load_common()
