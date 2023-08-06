import dataclasses
from dataclasses import dataclass, field

from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode


@dataclass
class Accumulation:
    enforce_complete_chunks: bool
    accumulated_assignments: list[str] = field(default_factory=list)
    accumulated_final_assignments: list[str] = field(default_factory=list)
    branch_fragments: list[str] = field(default_factory=list)
    core_match_fragments: list[str] = field(default_factory=list)


def accumulate_add_core_match(
        accumulation: Accumulation
        , core_node: LabelNode
        , branch: Branch
):

    core_match = branch.match_statement(core_node, with_assignment=False)
    new_acc = dataclasses.replace(
        accumulation
        , core_match_fragments=accumulation.core_match_fragments + [core_match]
    )
    return new_acc


def accumulate_add_value_match(
        accumulation: Accumulation
        , core_node: LabelNode
        , branch: Branch

):
    node_assignments = \
        branch.branch_node.property_fragments_by_cypher_assignments()
    branch_assignments = \
        branch.property_fragments_by_cypher_assignments()

    new_with_assignments = \
        [core_node.return_id] + \
        accumulation.accumulated_assignments + \
        list(node_assignments.values()) + \
        list(branch_assignments.values())

    branch_with_statement = f" with {' , '.join(new_with_assignments)}"

    value_match = branch.match_statement(core_node, with_assignment=True)
    new_assign = accumulation.accumulated_assignments + list(node_assignments.keys()) + list(branch_assignments.keys())
    new_branch_frags = \
        accumulation.branch_fragments + [value_match + branch_with_statement]


    new_final_assign = accumulation.accumulated_final_assignments + list(node_assignments.keys())
    new_acc = dataclasses.replace(
        accumulation
        , accumulated_assignments=new_assign
        , accumulated_final_assignments=new_final_assign
        , branch_fragments=new_branch_frags
    )

    return new_acc


def accumulate_branches(
        first_acc: Accumulation
        , core_node: LabelNode
        , branches: list[Branch]
):
    sorted_branches = sorted(branches, key=lambda b: b.optional)
    for branch in sorted_branches:
        if not branch.optional and first_acc.enforce_complete_chunks:
            first_acc = accumulate_add_core_match(
                first_acc
                , core_node
                , branch
            )
        first_acc = accumulate_add_value_match(
            first_acc
            , core_node
            , branch
        )
    return first_acc
