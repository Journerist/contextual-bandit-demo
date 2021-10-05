from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Ad:
    name: str
    ctr: float
    id: int

