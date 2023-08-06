def test_return_properties(plant_node,multiple_properties):
    assert ({'Plant.value':multiple_properties[0],
             'Plant.createdOn':multiple_properties[1]} == plant_node.return_properties())
