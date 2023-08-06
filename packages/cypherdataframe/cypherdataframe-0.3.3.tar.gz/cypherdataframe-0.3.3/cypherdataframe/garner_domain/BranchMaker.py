from dataclasses import dataclass, field

from cypherdataframe.garner_domain.properties_defaults import ID_PROP, PROP_TAGS
from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from abc import ABC, abstractmethod


@dataclass
class BranchMaker(ABC):
    props: list[Property]
    label: str
    relationship: str
    relationship_postfix: str | None
    required: bool
    archived: bool
    domain_label: str | None


    def return_id(self) -> str:
        if self.relationship_postfix != None:
            return f"{self.label}_{self.relationship_postfix}".lower()
        else:
            return f"{self.label}".lower()


    def node_label(self) -> str:
        if self.domain_label is not None:
            return f"{self.domain_label}:{self.label}"
        else:
            return self.label

    def to_branch(self) -> Branch:
        return Branch(
            relationship=self.relationship
            , away_from_core=not self.archived
            , branch_node=self.to_label_node()
            , optional=not self.required
        )

    def to_label_node(self) -> LabelNode:
        return LabelNode(
            return_id=self.return_id()
            , label=self.node_label()
            , properties=self.props
        )
