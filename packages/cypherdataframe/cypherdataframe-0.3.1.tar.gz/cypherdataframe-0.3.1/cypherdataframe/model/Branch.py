from dataclasses import dataclass

from cypherdataframe.model.LabelNode import LabelNode


# optional match(corenode)<back>-[<relationship>]-<forward>(<label>:<label>)

@dataclass(frozen=True)
class Branch:
    relationship: str | None
    away_from_core: bool | None
    branch_node: LabelNode
    optional: bool

    def property_fragments_by_cypher_assignments(self):
        if self.branch_node.collect:
            start_cap = "collect("
            end_cap = ")"
        else:
            start_cap = ""
            end_cap = ""

        if self.relationship == None:
            prop_by = {
               self.relationship_cypher_assignment(): (
                    f" {start_cap}{self.relationship_cypher_assignment()}{end_cap}"
                    f" as {self.relationship_cypher_assignment()} "
                )
            }
        else:
            prop_by = {}

        return prop_by

    def relationship_cypher_assignment(self) -> str:
        return f"{self.branch_node.label.lower()}_rel"

    def relationship_cypher_final_assignment(self) -> str | None:
        if self.relationship == None:
            return f"TYPE({self.relationship_cypher_assignment()}) as {self.relationship_cypher_assignment()}"
        else:
            return None

    def match_statement(self, corenode: LabelNode, with_assignment: bool):
        if self.away_from_core == True:
            back = ''
            forward = '>'
        elif self.away_from_core == False:
            back = '<'
            forward = ''
        else:
            back = ''
            forward = ''

        if with_assignment:
            node_id = self.branch_node.return_id
        else:
            node_id = ""

        if self.optional:
            optional = "optional"
        else:
            optional = ""

        if self.relationship == None:
            relationship_str = self.relationship_cypher_assignment()
        else:
            relationship_str = f":{self.relationship}"

        fragment = (
            f" {optional} " 
            f"match({corenode.return_id}){back}" 
            f"-[{relationship_str}]-"
            f"{forward}({node_id}:{self.branch_node.label})"
        )

        return fragment



