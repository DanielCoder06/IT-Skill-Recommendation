from dataclasses import dataclass, field


@dataclass
class JobRecord:
    title: str
    company: str
    description: str
    location: str
    url: str
    experience: str
    skills: list[str] = field(default_factory=list)