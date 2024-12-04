import pytest
from domain.exceptions import EntityNotFoundException, EntityAlreadyExistsException


def test_entity_not_found_exception():
    with pytest.raises(EntityNotFoundException, match="Entity not found!"):
        raise EntityNotFoundException("Entity not found!")


def test_entity_not_found_exception_message():
    exception = EntityNotFoundException("Entity not found!")
    assert exception.message == "Entity not found!"


def test_entity_already_exists_exception():
    with pytest.raises(EntityAlreadyExistsException, match="Entity already exists!"):
        raise EntityAlreadyExistsException("Entity already exists!")


def test_entity_already_exists_exception_message():
    exception = EntityAlreadyExistsException("Entity already exists!")
    assert exception.message == "Entity already exists!"
