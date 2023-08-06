from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ARCHIVED_ATTAINED_RELATIONSHIP, \
    ARCHIVED_ATTAINED_RETURN_POSTFIX
from cypherdataframe.model.Property import Property


@dataclass
class AttainedArchivedBranch(BranchMaker):
    props: list[Property]
    relationship: str = field(default_factory=lambda: ARCHIVED_ATTAINED_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: ARCHIVED_ATTAINED_RETURN_POSTFIX)
    required: bool = False
    archived: bool = True
    domain_label: str | None = None
