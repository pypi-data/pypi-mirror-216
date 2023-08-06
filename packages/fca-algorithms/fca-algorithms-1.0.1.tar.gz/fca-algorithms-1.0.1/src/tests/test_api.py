import pytest
from unittest import mock
from src.fca.api_models import Context

def test_inverted_hasse_calculation(create_objects_and_attributes):
    k_1 = create_objects_and_attributes
    ctx = Context(*k_1)
    l = ctx.get_lattice()
    for i, neighbours in enumerate(l.hasse):
        for j in neighbours:
            assert i in l.inverted_hasse[j]


def test_internal_method_called_once(create_objects_and_attributes):
    k_1 = create_objects_and_attributes
    ctx = Context(*k_1)
    l = ctx.get_lattice()
    with mock.patch.object(l, '_calculate_inverted_hasse', wraps=l._calculate_inverted_hasse) as wrapped_l:
        i = l.inverted_hasse
        i = l.inverted_hasse
    wrapped_l.assert_called_once()
