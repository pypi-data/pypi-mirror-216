import pytest

from cypherdataframe.model.LabelNode import LabelNode


@pytest.fixture
@pytest.mark.usefixtures("multiple_properties")
def plant_node(multiple_properties) -> LabelNode:
    return LabelNode('Plant', multiple_properties)


@pytest.fixture
@pytest.mark.usefixtures("material_properties")
def material_node(material_properties) -> LabelNode:
    return LabelNode('Material', material_properties)
