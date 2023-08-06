import pytest

from loggy.exceptions import MutuallyExclusiveArgumentsError, exclusive_args


def test_mutually_exclusive_arguments_raises():

    @exclusive_args(["one", "two"])
    def inner(one: int = None, two: int = None) -> int:
        return 0

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(one=1, two=2)


def test_multiple_mutually_exclusive_arguments_raises():

    @exclusive_args(["one", "two", "three"])
    def inner(one: int = None, two: int = None, three: int = None) -> int:
        return 0

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(one=1, two=2)

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(one=1, three=2)

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(two=1, three=2)

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(one=1, two=2, three=3)


def test_combined_mutually_exclusive_arguments_raises():

    @exclusive_args(["one", "two"])
    @exclusive_args(["three", "four"])
    def inner(one: int = None,
              two: int = None,
              three: int = None,
              four: int = None) -> int:
        return 0

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(one=1, two=2)

    with pytest.raises(MutuallyExclusiveArgumentsError):
        inner(three=3, four=4)

