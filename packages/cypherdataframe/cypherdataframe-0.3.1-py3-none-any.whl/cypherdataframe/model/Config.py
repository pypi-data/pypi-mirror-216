import configparser
from dataclasses import dataclass
from dacite import from_dict

@dataclass(frozen=True)
class Config:
    neo4j_url: str
    neo4j_password: str
    neo4j_username: str

