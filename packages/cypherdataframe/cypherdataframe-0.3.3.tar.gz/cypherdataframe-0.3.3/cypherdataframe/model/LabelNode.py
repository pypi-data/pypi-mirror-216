from dataclasses import dataclass

from cypherdataframe.model.Property import Property


@dataclass(frozen=True)
class LabelNode:
    return_id: str
    label: str
    properties: list[Property]
    collect: bool = False

    def properties_by_final_assigment(self):
        return {prop.final_assigment(self): prop for prop in self.properties}

    def property_fragments_by_cypher_assignments(self):
        if self.collect:
            start_cap = "collect("
            end_cap = ")"
        else:
            start_cap = ""
            end_cap = ""

        prop_by = {
            prop.final_assigment(self): (
                f" {start_cap}{prop.cypher_assigment(self)}{end_cap}" 
                f" as {prop.final_assigment(self)} "
            )
            for prop in self.properties
        }

        return prop_by
