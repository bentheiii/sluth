from pytest import fixture

from sluth import NodeWalk


@fixture()
def fringe_walker():
    return NodeWalk.from_file("tests/data/fringe.py")


def test_fringe_find_class_afunc(fringe_walker):
    needle = fringe_walker["afoo"]

    assert needle.lineno == 3
    assert needle.col_offset == 0
    assert needle.end_lineno == 4
    assert needle.end_col_offset == 17


def test_fringe_find_class_classvar(fringe_walker):
    needle = fringe_walker["Bar"]["a"]

    assert needle.lineno == 8
    assert needle.col_offset == 4
    assert needle.end_lineno == 9
    assert needle.end_col_offset == 17


def test_fringe_find_asimport(fringe_walker):
    needle = fringe_walker["gold"]

    assert needle.lineno == 15
    assert needle.col_offset == 0
    assert needle.end_lineno == 15
    assert needle.end_col_offset == 20


def test_fringe_find_import(fringe_walker):
    needle = fringe_walker["steel"]

    assert needle.lineno == 14
    assert needle.col_offset == 0
    assert needle.end_lineno == 14
    assert needle.end_col_offset == 12


def test_fringe_find_asfromimport(fringe_walker):
    needle = fringe_walker["tin"]

    assert needle.lineno == 16
    assert needle.col_offset == 0
    assert needle.end_lineno == 16
    assert needle.end_col_offset == 31


def test_fringe_find_fromimport(fringe_walker):
    needle = fringe_walker["bronze"]

    assert needle.lineno == 17
    assert needle.col_offset == 0
    assert needle.end_lineno == 17
    assert needle.end_col_offset == 24


def test_fringe_find_forvar(fringe_walker):
    needle = fringe_walker["i"]

    assert needle.lineno == 19
    assert needle.col_offset == 0
    assert needle.end_lineno == 19
    assert needle.end_col_offset == 18


def test_fringe_find_forvar_tup(fringe_walker):
    needle = fringe_walker["i0"]

    assert needle.lineno == 22
    assert needle.col_offset == 0
    assert needle.end_lineno == 22
    assert needle.end_col_offset == 23


def test_fringe_find_aforvar(fringe_walker):
    needle = fringe_walker["ai"]

    assert needle.lineno == 25
    assert needle.col_offset == 0
    assert needle.end_lineno == 25
    assert needle.end_col_offset == 25


def test_fringe_find_aforvar_tup(fringe_walker):
    needle = fringe_walker["ai1"]

    assert needle.lineno == 28
    assert needle.col_offset == 0
    assert needle.end_lineno == 28
    assert needle.end_col_offset == 31


def test_fringe_find_var_in_for(fringe_walker):
    needle = fringe_walker["g"]

    assert needle.lineno == 29
    assert needle.col_offset == 4
    assert needle.end_lineno == 29
    assert needle.end_col_offset == 10


def test_fringe_find_withvar(fringe_walker):
    needle = fringe_walker["my_file"]

    assert needle.lineno == 35
    assert needle.col_offset == 0
    assert needle.end_lineno == 35
    assert needle.end_col_offset == 32


def test_fringe_find_awithvar(fringe_walker):
    needle = fringe_walker["my_afile"]

    assert needle.lineno == 38
    assert needle.col_offset == 0
    assert needle.end_lineno == 38
    assert needle.end_col_offset == 39


def test_fringe_find_withvars(fringe_walker):
    needle = fringe_walker["my_file1"]

    assert needle.lineno == 41
    assert needle.col_offset == 0
    assert needle.end_lineno == 41
    assert needle.end_col_offset == 64


def test_fringe_find_vars_in_with(fringe_walker):
    needle = fringe_walker["t"]

    assert needle.lineno == 36
    assert needle.col_offset == 4
    assert needle.end_lineno == 36
    assert needle.end_col_offset == 22


def test_fringe_find_withvar_tup(fringe_walker):
    needle = fringe_walker["my_filep0"]

    assert needle.lineno == 50
    assert needle.col_offset == 0
    assert needle.end_lineno == 50
    assert needle.end_col_offset == 47


def test_fringe_find_awithvar_tup(fringe_walker):
    needle = fringe_walker["my_afilep0"]

    assert needle.lineno == 53
    assert needle.col_offset == 0
    assert needle.end_lineno == 53
    assert needle.end_col_offset == 63
