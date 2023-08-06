from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property


def branches_from_labels(
        relationship: str | None,
        away_direction: bool,
        labels: list[str],
        properties: list[Property],
        collect: bool = False,
        optional: bool = True
) -> list[Branch]:
    return [
        Branch(
            relationship
            , away_direction
            , LabelNode(
                return_id=label.replace(":", "_")
                , label=label
                , properties=properties
                , collect=collect
            )
            , optional=optional)
        for label in labels
    ]


