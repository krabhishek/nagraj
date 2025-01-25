"""Tests for BaseValueObject class."""

from dataclasses import dataclass, fields
from decimal import Decimal
from typing import Optional

import pytest

from {{ cookiecutter.project_slug }}.common.base.value_object import BaseValueObject


@pytest.mark.no_collect  # Ignore this class during test collection
@dataclass(frozen=True)
class EmptyValueObject(BaseValueObject):
    """A value object with no fields."""

    pass


@pytest.mark.no_collect  # Ignore this class during test collection
@dataclass(frozen=True)
class NestedValueObject(BaseValueObject):
    """A value object that will be nested in another."""

    value: int


@pytest.mark.no_collect  # Ignore this class during test collection
@dataclass(frozen=True)
class ComplexValueObject(BaseValueObject):
    """A value object with various field types."""

    text: str
    number: int
    decimal: Decimal
    nested: NestedValueObject
    optional: Optional[str] = None


@pytest.mark.no_collect  # Ignore this class during test collection
@dataclass(frozen=True)
class TestValueObject(BaseValueObject):
    """Test implementation of BaseValueObject."""

    name: str
    value: int


def test_value_object_equality():
    """Test that value objects are equal when their attributes are equal."""
    vo1 = TestValueObject(name="test", value=1)
    vo2 = TestValueObject(name="test", value=1)
    vo3 = TestValueObject(name="different", value=1)

    # Test equality with same values
    assert vo1 == vo2
    assert vo1 != vo3

    # Test equality with non-BaseValueObject types
    # Python's equality is symmetric, so when comparing with non-value objects,
    # we return NotImplemented to let the other object handle the comparison
    assert vo1.__eq__("not a value object") is NotImplemented
    assert vo1.__eq__(None) is NotImplemented
    assert vo1.__eq__(object()) is NotImplemented
    assert vo1.__eq__({"name": "test", "value": 1}) is NotImplemented
    assert vo1 is not vo2  # Different instances

    # Test __eq__ explicitly with value objects
    assert vo1.__eq__(vo2) is True
    assert vo1.__eq__(vo3) is False


def test_value_object_hash():
    """Test that value objects can be used as dictionary keys."""
    vo1 = TestValueObject(name="test", value=1)
    vo2 = TestValueObject(name="test", value=1)
    vo3 = TestValueObject(name="different", value=1)

    # Test hash equality for equal objects
    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)

    # Test using value objects as dictionary keys
    d = {vo1: "value1"}
    assert (
        d[vo2] == "value1"
    )  # vo2 is equal to vo1, so it should retrieve the same value


def test_empty_value_object():
    """Test value objects with no fields."""
    vo1 = EmptyValueObject()
    vo2 = EmptyValueObject()

    # Test equality and hash with empty fields
    assert vo1 == vo2
    assert hash(vo1) == hash(vo2)
    assert hash(vo1) == hash(tuple())  # Empty tuple for empty fields
    assert repr(vo1) == "EmptyValueObject()"


def test_complex_value_object_equality():
    """Test equality with complex nested value objects."""
    nested1 = NestedValueObject(value=42)
    nested2 = NestedValueObject(value=42)
    nested3 = NestedValueObject(value=43)

    vo1 = ComplexValueObject(
        text="test",
        number=1,
        decimal=Decimal("10.5"),
        nested=nested1,
        optional="present",
    )
    vo2 = ComplexValueObject(
        text="test",
        number=1,
        decimal=Decimal("10.5"),
        nested=nested2,  # Different instance but equal value
        optional="present",
    )
    vo3 = ComplexValueObject(
        text="test",
        number=1,
        decimal=Decimal("10.5"),
        nested=nested3,  # Different value
        optional="present",
    )

    assert vo1 == vo2
    assert vo1 != vo3
    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)


def test_value_object_immutability():
    """Test that value objects are immutable."""
    vo = TestValueObject(name="test", value=1)

    # Attempt to modify the object should raise an error
    with pytest.raises(AttributeError):
        vo.name = "new name"  # type: ignore


def test_value_object_repr():
    """Test the string representation of value objects."""
    vo = TestValueObject(name="test", value=1)

    # Test __repr__ explicitly
    repr_value = vo.__repr__()
    assert isinstance(repr_value, str)
    assert repr_value == "TestValueObject(name='test', value=1)"

    # Test complex value object representation with various field types
    nested = NestedValueObject(value=42)
    complex_vo = ComplexValueObject(
        text="test", number=1, decimal=Decimal("10.5"), nested=nested, optional=None
    )
    complex_repr = complex_vo.__repr__()

    # Test each field's representation
    assert "ComplexValueObject" in complex_repr
    assert "text='test'" in complex_repr
    assert "number=1" in complex_repr
    assert "decimal=Decimal('10.5')" in complex_repr
    assert "nested=NestedValueObject(value=42)" in complex_repr
    assert "optional=None" in complex_repr

    # Test special characters in string fields
    special_vo = TestValueObject(name="test'with\"quotes", value=1)
    special_repr = special_vo.__repr__()
    assert "name='test\\'with\"quotes'" in special_repr


def test_value_object_in_set():
    """Test that value objects can be used in sets."""
    vo1 = TestValueObject(name="test", value=1)
    vo2 = TestValueObject(name="test", value=1)
    vo3 = TestValueObject(name="different", value=1)

    s = {vo1, vo2, vo3}
    # Since vo1 and vo2 are equal, the set should only contain 2 items
    assert len(s) == 2
    assert vo1 in s
    assert vo2 in s
    assert vo3 in s


def test_value_object_with_none_values():
    """Test value objects with optional/None values."""
    vo1 = ComplexValueObject(
        text="test",
        number=1,
        decimal=Decimal("10.5"),
        nested=NestedValueObject(value=42),
        optional=None,
    )
    vo2 = ComplexValueObject(
        text="test",
        number=1,
        decimal=Decimal("10.5"),
        nested=NestedValueObject(value=42),
        optional=None,
    )

    assert vo1 == vo2
    assert hash(vo1) == hash(vo2)
    assert vo1 is not vo2


def test_value_object_dict_comparison():
    """Test that value objects with the same attributes have equal __dict__ values."""
    vo1 = TestValueObject(name="test", value=1)
    vo2 = TestValueObject(name="test", value=1)

    assert vo1.__dict__ == vo2.__dict__
    assert vo1.__dict__ != {"name": "different", "value": 1}


def test_value_object_field_access():
    """Test that field access works correctly in hash and repr methods."""
    vo = TestValueObject(name="test", value=1)

    # Test field access in hash
    field_values = tuple(getattr(vo, field.name) for field in fields(vo))
    assert hash(vo) == hash(field_values)

    # Test field access in repr
    field_reprs = [f"{field.name}={getattr(vo, field.name)!r}" for field in fields(vo)]
    expected_repr = f"TestValueObject({', '.join(field_reprs)})"
    assert repr(vo) == expected_repr


def test_value_object_explicit_method_calls():
    """Test explicit calls to magic methods to ensure coverage."""
    vo = TestValueObject(name="test", value=1)

    # Test __eq__ with various types
    assert vo.__eq__(vo) is True
    assert vo.__eq__(None) is NotImplemented
    assert vo.__eq__("not a value object") is NotImplemented
    assert vo.__eq__({"name": "test", "value": 1}) is NotImplemented

    # Test __hash__
    hash_value = vo.__hash__()
    assert isinstance(hash_value, int)
    assert hash_value == hash(tuple(getattr(vo, field.name) for field in fields(vo)))

    # Test __repr__
    repr_value = vo.__repr__()
    assert isinstance(repr_value, str)
    assert repr_value == "TestValueObject(name='test', value=1)"
