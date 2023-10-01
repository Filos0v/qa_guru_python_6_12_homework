from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    phone: str
    email: str
    gender: str
    subjects: list
    birth_date: object
    hobbies: str
    picture: str
    state: str
    city: str
    current_address: str