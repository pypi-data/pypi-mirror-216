import pytest

from src.fca.rca.models import Relation


@pytest.fixture
def create_objects_and_attributes():
    O = ['Tg05', 'Tg05FX', 'Flxtra', 'Hxr']
    A = ['Effect', 'Power', 'Control', 'Short']
    I = [
        [0, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 0, 1, 0],
        [1, 0, 1, 0],
    ]
    return O, A, I


@pytest.fixture
def create_objects_and_attributes_2():
    O = ['1', '2', '3', '4', '5']
    A = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    I = [
        [1, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0],
    ]
    return O, A, I


@pytest.fixture
def create_relation_between_0_and_1():
    I = [
        # object in index 0 is related with 0 and also with 2 of the other
        # context
        set([0, 2]),
        # object in index 1 is related with 0, 2 and 4 of the other context
        set([0, 2, 4]),
        set([0, 3]),
        set([1, 2]),
    ]
    return Relation(I, [0, 1])
