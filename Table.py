from Person import Person

class Table:

    def __init__(self, number: int, number_of_people: int) -> None:
        self.number = number
        self.number_of_people = number_of_people
        self.people: list[Person] = []

    def add_person(self, person: Person) -> None:
        self.people.append(person)

    @property
    def is_full(self) -> bool:
        return len(self.people) >= self.number_of_people