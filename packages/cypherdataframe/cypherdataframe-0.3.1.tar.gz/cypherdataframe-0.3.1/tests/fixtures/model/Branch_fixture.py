import pytest

from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode


@pytest.fixture
@pytest.mark.usefixtures("plant_node")
def plant_branch(plant_node) -> Branch:
    return Branch('REFERENCED_AS', True, plant_node)
