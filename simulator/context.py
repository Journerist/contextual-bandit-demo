from dataclasses import dataclass
from ad import Ad

@dataclass
class Context:
    name: str
    ctr_multiplier: dict[Ad, float]
