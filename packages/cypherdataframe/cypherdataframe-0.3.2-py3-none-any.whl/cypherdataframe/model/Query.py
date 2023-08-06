from dataclasses import dataclass, field
from typing import Optional

from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.QueryAccumulation import Accumulation, \
    accumulate_add_value_match, accumulate_add_core_match, accumulate_branches


@dataclass(frozen=True)
class Query:
    core_node: LabelNode
    branches: list[Branch]
    skip: int | None = field(default_factory=lambda: None)
    limit: int | None = field(default_factory=lambda: None)
    enforce_complete_chunks: bool = field(default_factory=lambda: True)

    def all_properties_by_final_assigment(self) -> dict[str, Property]:

        branch_properties = {}

        for branch in self.branches:
            branch_properties.update(
                branch.branch_node.properties_by_final_assigment()
            )

        branch_properties.update(self.core_node.properties_by_final_assigment())
        return branch_properties

    def to_cypher(self) -> str:

        first_core_match = f'match({self.core_node.return_id}:{self.core_node.label}) '


        if all([branch.away_from_core for branch in self.branches]):
            scan_core_str = ""
        else:
            scan_core_str = f"USING SCAN {self.core_node.return_id}:{self.core_node.label}"
        accumulated_fragments = Accumulation(
            core_match_fragments=[first_core_match, scan_core_str],
            enforce_complete_chunks=self.enforce_complete_chunks
        )

        accumulated_fragments = accumulate_branches(
            accumulated_fragments
            , self.core_node
            , self.branches
        )

        skip_string = f"skip {self.skip}" if self.skip is not None else ""
        limit_string = f"limit {self.limit}" if self.limit is not None else ""

        core_node_return_assignments = list(
            self.core_node.property_fragments_by_cypher_assignments().values()
        )

        return_fragment = ",".join(
            core_node_return_assignments +
            accumulated_fragments.accumulated_final_assignments
        )




        fragments = \
            accumulated_fragments.core_match_fragments + \
            [f'with distinct {self.core_node.return_id}'] + \
            [skip_string] + \
            [limit_string] + \
            accumulated_fragments.branch_fragments + \
            ["return "] + \
            [return_fragment] + \
            [";"]

        final_query = " ".join(fragments)
        return final_query
