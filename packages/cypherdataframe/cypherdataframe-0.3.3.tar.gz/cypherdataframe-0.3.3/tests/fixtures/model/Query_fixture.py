import pytest
import pytest
from cypherdataframe.model.Query import Query


@pytest.fixture
@pytest.mark.usefixtures("plant_branch", "material_node")
def query_material_1(plant_branch, material_node) -> Query:
    return Query(material_node, [plant_branch], skip=0, limit=10000)
