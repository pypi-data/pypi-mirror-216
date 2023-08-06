from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import FORECASTED_RETURN_POSTFIX, FORECASTED_RELATIONSHIP
from cypherdataframe.model.Property import Property


@dataclass
class ForecastedBranch(BranchMaker):
    props: list[Property]
    relationship: str = field(default_factory=lambda: FORECASTED_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: FORECASTED_RETURN_POSTFIX)
    required: bool = False
    archived: bool = False
    domain_label: str | None = None

