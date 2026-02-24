from dataclasses import dataclass


@dataclass
class GlueType:
    id: str
    name: str
    description: str = ""
