from dataclasses import dataclass

@dataclass
class MenuItem:
    id: int
    name: str
    description: str
    price: float
    category: str