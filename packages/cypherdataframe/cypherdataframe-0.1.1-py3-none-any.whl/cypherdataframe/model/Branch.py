from dataclasses import dataclass

from cypherdataframe.model.LabelNode import LabelNode


# optional match(corenode)<back>-[<relationship>]-<forward>(<label>:<label>)

@dataclass(frozen=True)
class Branch:
    relationship: str
    away_direction: bool
    branch_node: LabelNode

    def cypher_fragment(self) -> str:
        if self.away_direction:
            back = ''
            forward = '>'
        else:
            back = '<'
            forward = ''

        return f"""optional match(corenode){back}-[:{self.relationship}]-{forward}({self.branch_node.label}:{self.branch_node.label})"""
