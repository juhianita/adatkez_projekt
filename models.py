#pip install faker openpyxl

from dataclasses import dataclass, field

@dataclass
class Daycare:
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    city: str = field(repr=True, compare=False)
    daily_fee: int = field(repr=True, compare=False)

@dataclass
class Person:
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)
    daycare_id: str = field(default="", repr=True, compare=False)

@dataclass
class Pet:
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    species: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    owner_id: str = field(repr=True, compare=False)
