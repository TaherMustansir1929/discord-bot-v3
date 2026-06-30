from dataclasses import dataclass
from typing import Any, Optional, Union


@dataclass
class Repository:
    id: int
    name: str
    owner: str
    owner_avatar: str
    stars: int
    forks: int
    watchers: int
    description: str
    language: str
    topics: list[str]
    updated_at: str
    url: str
    license: str
    has_issues: bool
