from cypherdataframe.branch_maker import branches_from_labels
from cypherdataframe.model.Branch import Branch
from cypherdataframe.model.LabelNode import LabelNode


def test_branches_from_labels(reference_properties):
    reference_labels = [
        'Plant',
        'PoNumber',
        'PoLine',
        'ReqNumber',
        'ReqLine',
        'ResNumber',
        'ResLine'
    ]
    reference_branches = branches_from_labels(
        "REFERENCED_AS", True,
        reference_labels,
        reference_properties
    )
    expected = [
        Branch('REFERENCED_AS', True, LabelNode('Plant', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('PoNumber', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('PoLine', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('ReqNumber', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('ReqLine', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('ResNumber', reference_properties)),
        Branch('REFERENCED_AS', True,
               LabelNode('ResLine', reference_properties))
    ]
    assert (expected == reference_branches)
