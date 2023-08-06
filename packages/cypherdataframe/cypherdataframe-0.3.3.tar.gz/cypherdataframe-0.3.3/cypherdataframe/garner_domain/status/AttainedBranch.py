from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ATTAINED_RELATIONSHIP, ATTAINED_RETURN_POSTFIX
from cypherdataframe.model.Property import Property



@dataclass
class AttainedBranch(BranchMaker):
    props: list[Property]
    relationship: str = field(default_factory=lambda: ATTAINED_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: ATTAINED_RETURN_POSTFIX)
    required: bool = False
    archived: bool = False
    domain_label: str | None = None

