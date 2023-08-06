def test_cypher_fragment(plant_branch):
    result ="optional match(corenode)-[:REFERENCED_AS]->(Plant:Plant)"
    assert(plant_branch.cypher_fragment()==result)

