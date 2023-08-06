from dataclasses import dataclass


@dataclass
class DomainRecord:
    data: str
    name: str
    port: int
    priority: int
    protocol: str
    service: str
    ttl: int
    type: str
    weight: int