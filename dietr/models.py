from dataclasses import dataclass, fields


@dataclass
class User(object):
    id: int
    handle: string

    mail: string
    first_name: string
    middle_name: string
    last_name: string

    allergies: list = []
    ingredients: list = []


@dataclass
class Ingredient(object):
    id: int

    name: string

    allergies: list = []


@dataclasses
class Allergy(object):
    id: int

    name: string


@dataclass
class Recipe(object):
    id: int

    name: string
    url: string

    allergies: list = []
    ingredients: list = []
