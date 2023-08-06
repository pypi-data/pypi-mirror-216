from datetime import datetime

import pytest

from cypherdataframe.model.Property import Property


@pytest.fixture
def no_property() -> list[Property]:
    return []


@pytest.fixture
def single_property() -> list[Property]:
    return [Property('value', str)]


@pytest.fixture
def multiple_properties() -> list[Property]:
    return [
        Property('value', str)
        ,   Property('createdOn', datetime)
    ]


@pytest.fixture
def multiple_with_date_property() -> list[Property]:
    return [Property('id', str), Property('createdOn', datetime)]


@pytest.fixture
def material_properties() -> list[Property]:
    return [
        Property('id', str)
        ,   Property('createdOn', datetime)
    ]


@pytest.fixture
def reference_properties() -> list[Property]:
    return [
        Property('value', str)
        ,   Property('createdOn', datetime)
    ]


@pytest.fixture
def status_properties() -> list[Property]:
    return [
        Property('occursOn', str)
        ,   Property('createdOn', datetime)
    ]
