def test_cypher_query(query_material_1):
    q = query_material_1.to_cypher()
    print(q)
    assert(True)


