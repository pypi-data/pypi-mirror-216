from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import \
    TRANSFER_RELATIONSHIP, \
    TRANSFER_RETURN_ID, TRANSFER_LABEL
from cypherdataframe.model.Property import Property


@dataclass
class TransferBranch(BranchMaker):
    props: list[Property]
    label: str = TRANSFER_LABEL
    relationship: str = field(default_factory=lambda: TRANSFER_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: TRANSFER_RETURN_ID)
    required: bool = False
    archived: bool = True
    domain_label: str | None = None
