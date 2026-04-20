from Person import Person

class Table:

    def __init__(self, number: int, number_of_people: int) -> None:
        """Initialises table object"""
        self.number = number
        self.number_of_people = number_of_people
        self.people: list[Person] = []

    def add_person(self, person: Person) -> None:
        """Adds a person to the table"""
        self.people.append(person)