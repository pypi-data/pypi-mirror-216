from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property


def branches_from_labels(
        relationship: str,
        away_direction: bool,
        labels: list[str],
        properties: list[Property]
) -> list[Branch]:
    return [
        Branch(relationship, away_direction, LabelNode(label, properties))
        for label in labels
    ]
