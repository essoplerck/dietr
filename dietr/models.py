from dataclasses import dataclass, field


@dataclass
class User(object):
    id: int
    handle: string

    mail: string
    first_name: string
    middle_name: string
    last_name: string

    allergies: list = field(default_factory=list, init=False)
    ingredients: list = field(default_factory=list, init=False)


@dataclass
class Recipe(object):
    id: int

    name: string
    url: string

    allergies: list = []
    ingredients: list = []
