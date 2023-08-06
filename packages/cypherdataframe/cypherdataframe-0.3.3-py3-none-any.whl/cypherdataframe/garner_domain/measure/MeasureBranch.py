from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import \
    MEASURE_RELATIONSHIP, MEASURE_RETURN_POSTFIX
from cypherdataframe.model.Property import Property


@dataclass
class MeasureBranch(BranchMaker):
    domain_label: str | None = None
    props_tag: str | None = "Measure"
    props: list[Property] | None = None
    not_archived: bool | None = True
    relationship: str = field(default_factory=lambda: MEASURE_RELATIONSHIP)
    relationship_postfix: str = field(default_factory=lambda: MEASURE_RETURN_POSTFIX)

