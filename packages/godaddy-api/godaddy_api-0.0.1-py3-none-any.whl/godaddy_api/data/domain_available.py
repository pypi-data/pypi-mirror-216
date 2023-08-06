from dataclasses import dataclass


@dataclass
class DomainAvailable:
    available: bool
    currency: str
    definitive: bool
    domain: str
    period: int
    price: int
