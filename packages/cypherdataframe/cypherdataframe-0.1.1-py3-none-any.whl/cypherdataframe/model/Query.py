from dataclasses import dataclass
import functools
import operator
from typing import Optional

from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property


@dataclass(frozen=True)
class Query:
    core_node: LabelNode
    branches: list[Branch]
    skip: Optional[int]
    limit: Optional[int]

    def property_names(self) -> dict[str, Property]:
        property_names = {f"corenode.{prop.label}": prop
                          for prop in self.core_node.properties}
        return property_names | functools.reduce(
            lambda d, src: d.update(src) or d,
            [
                branch.branch_node.return_properties()
                for branch in self.branches
            ],
            {}
        )

    def cypher_query(self) -> str:
        skip_string = f"skip {self.skip}" if self.skip is not None else ""
        limit_string = f"limit {self.limit}" if self.limit is not None else ""
        matches = [
                      f'match(corenode:{self.core_node.label}) ' +
                      f'with corenode {skip_string} {limit_string}'
                  ] + [
                      branch.cypher_fragment() for branch in self.branches
                  ]

        return_fragment = "return " + ",".join(self.property_names()) + ';'
        fragments = matches + [return_fragment]

        return " ".join(fragments)
