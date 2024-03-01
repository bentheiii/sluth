from pytest import raises

from sluth.walker import NodeWalk


def test_reuse(monkeypatch):
    walker = NodeWalk.from_source("a = 1")
    assert walker["a"]
    monkeypatch.setattr(NodeWalk, "_get_children", None)
    assert walker["a"]


def test_missing():
    walker = NodeWalk.from_source("a = 1")
    with raises(KeyError):
        walker["b"]
    assert not walker.get_many("b")


def test_multi():
    walker = NodeWalk.from_source("a = 1\na = 2")
    with raises(ValueError):
        walker["a"]
    m0, m1 = walker.get_many("a")
    assert m0.lineno == 1
    assert m1.lineno == 2
