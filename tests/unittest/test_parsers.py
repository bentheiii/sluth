from pytest import fixture

from sluth import NodeWalk


@fixture()
def walker_parsers():
    return NodeWalk.from_file("tests/data/parsers.py")


def test_parsers_find_class(walker_parsers):
    needle = walker_parsers["BoolParser"]

    assert needle.lineno == 110
    assert needle.col_offset == 0
    assert needle.end_lineno == 150
    assert needle.end_col_offset == 27


def test_parsers_find_method(walker_parsers):
    needle = walker_parsers["BoolParser"]["__init__"]

    assert needle.lineno == 115
    assert needle.col_offset == 4
    assert needle.end_lineno == 137
    assert needle.end_col_offset == 30


def test_parsers_find_glob_var(walker_parsers):
    needle = walker_parsers["no_fallback"]

    assert needle.lineno == 304
    assert needle.col_offset == 0
    assert needle.end_lineno == 304
    assert needle.end_col_offset == 36


def test_parsers_find_method_with_decorator(walker_parsers):
    needle = walker_parsers["MatchParser"]["case_insensitive"]

    assert needle.lineno == 339
    assert needle.col_offset == 4
    assert needle.end_lineno == 344
    assert needle.end_col_offset == 39


def test_parsers_find_function(walker_parsers):
    needle = walker_parsers["needle_to_pattern"]

    assert needle.lineno == 165
    assert needle.col_offset == 0
    assert needle.end_lineno == 168
    assert needle.end_col_offset == 12


def test_parsers_find_true_assignment(walker_parsers):
    needle = walker_parsers["parser_special_superclasses"]

    assert needle.lineno == 66
    assert needle.col_offset == 0
    assert needle.end_lineno == 66
    assert needle.end_col_offset == 70


def test_no_inners(walker_parsers):
    needle = walker_parsers.get_many("__init__")

    assert not needle