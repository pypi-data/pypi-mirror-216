from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ID_PROP
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query

@dataclass
class LogisticsTableQuery:
    branchMakers: list[BranchMaker]
    label: str
    return_id: str = "l"
    props: list[Property] = field(default_factory=lambda: [ID_PROP])
    def to_query(self, skip: int | None = None, limit: int | None = None):
        return Query(
            LabelNode(
                return_id=self.return_id,
                label=self.label,
                properties=self.props,
                collect=False
            ),
            branches=[b.to_branch() for b in self.branchMakers],
            skip=skip,
            limit=limit
        )



