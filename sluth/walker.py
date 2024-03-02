from __future__ import annotations

from ast import (
    AST,
    AnnAssign,
    Assign,
    AsyncFor,
    AsyncFunctionDef,
    AsyncWith,
    ClassDef,
    For,
    FunctionDef,
    Import,
    ImportFrom,
    NodeVisitor,
    With,
    parse,
)
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any


class Visitor(NodeVisitor):
    def __init__(self, top_node: AST) -> None:
        super().__init__()
        self.top_node = top_node
        self.children: dict[str, list[AST]] = defaultdict(list)

    # note, currently we don't support named expressions in definitions, which I'm going to go ahead and call a feature
    def visit_ClassDef(self, node: ClassDef):
        if node is self.top_node:
            super().generic_visit(node)
        else:
            self.children[node.name].append(node)

    def visit_FunctionDef(self, node: FunctionDef):
        self.children[node.name].append(node)

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef):
        self.children[node.name].append(node)

    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if hasattr(target, "elts"):
                for elt in target.elts:
                    self.children[elt.id].append(node)
            elif hasattr(target, "id"):
                self.children[target.id].append(node)

    def visit_AnnAssign(self, node: AnnAssign):
        if hasattr(node.target, "id"):
            self.children[node.target.id].append(node)

    def visit_TypeAlias(self, node: Any):
        # typealias is only available in 3.12+
        self.children[node.name].append(node)

    def visit_Import(self, node: Import) -> Any:
        for alias in node.names:
            if alias.asname is not None:
                self.children[alias.asname].append(node)
            else:
                self.children[alias.name].append(node)

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        for alias in node.names:
            if alias.asname is not None:
                self.children[alias.asname].append(node)
            elif alias.name != "*":
                self.children[alias.name].append(node)

    def visit_For(self, node: For) -> Any:
        if hasattr(node.target, "id"):
            self.children[node.target.id].append(node)
        elif hasattr(node.target, "elts"):
            for elt in node.target.elts:
                self.children[elt.id].append(node)
        return self.generic_visit(node)

    def visit_With(self, node: With) -> Any:
        for item in node.items:
            if not (v := item.optional_vars):
                continue
            if hasattr(v, "id"):
                self.children[v.id].append(node)
            elif hasattr(v, "elts"):
                for elt in v.elts:
                    self.children[elt.id].append(node)
            else:
                # according to the specs this shouldn't happen
                pass
        return self.generic_visit(node)

    def visit_AsyncFor(self, node: AsyncFor) -> Any:
        if hasattr(node.target, "id"):
            self.children[node.target.id].append(node)
        elif hasattr(node.target, "elts"):
            for elt in node.target.elts:
                self.children[elt.id].append(node)
        return self.generic_visit(node)

    def visit_AsyncWith(self, node: AsyncWith) -> Any:
        for item in node.items:
            if not (v := item.optional_vars):
                continue
            if hasattr(v, "id"):
                self.children[v.id].append(node)
            elif hasattr(v, "elts"):
                for elt in v.elts:
                    self.children[elt.id].append(node)
            else:
                # according to the specs this shouldn't happen
                pass
        return self.generic_visit(node)


@dataclass
class NodeWithOffset:
    node: AST
    lineno_offset: int = 0
    col_offset_offset: int = 0
    end_lineno_offset: int = 0
    end_col_offset_offset: int = 0

    @property
    def lineno(self) -> int:
        return self.node.lineno + self.lineno_offset

    @property
    def col_offset(self) -> int:
        return self.node.col_offset + self.col_offset_offset

    @property
    def end_lineno(self) -> int | None:
        if self.node.end_lineno is None:
            return None
        return self.node.end_lineno + self.end_lineno_offset

    @property
    def end_col_offset(self) -> int | None:
        if self.node.end_col_offset is None:
            return None
        return self.node.end_col_offset + self.end_col_offset_offset


class NodeWalk:
    def __init__(self, node: AST):
        self.node = node
        self._children: dict[str, list[NodeWalk]] | None = None

    def _get_children(self) -> dict[str, list[NodeWalk]]:
        visitor = Visitor(self.node)
        visitor.visit(self.node)
        return {k: [type(self)(n) for n in v] for k, v in visitor.children.items()}

    def children(self) -> Mapping[str, Sequence[NodeWalk]]:
        if self._children is None:
            self._children = self._get_children()
        return self._children

    def __getitem__(self, name: str) -> NodeWalk:
        name, _, suffix = name.partition(".")

        candidates = self.children().get(name, ())
        if not candidates:
            raise KeyError(f"No nodes with the name {name}, found names: {sorted(self.children().keys())}")
        if len(candidates) > 1:
            raise ValueError(f"Multiple nodes with the name {name}")
        ret = candidates[0]
        if suffix:
            return ret[suffix]
        return ret

    def get_last(self, name: str) -> NodeWalk:
        name, _, suffix = name.partition(".")

        candidates = self.children().get(name, ())
        if not candidates:
            raise KeyError(f"No nodes with the name {name}, found names: {sorted(self.children().keys())}")
        ret = candidates[-1]
        if suffix:
            return ret.get_last(suffix)
        return ret

    def get_many(self, name: str) -> Sequence[NodeWalk]:
        return self.children().get(name, ())

    def _start_node(self) -> NodeWithOffset:
        if decorators := getattr(self.node, "decorator_list", ()):
            return NodeWithOffset(decorators[0], col_offset_offset=-1)
        return NodeWithOffset(self.node)

    def _end_node(self) -> NodeWithOffset:
        if iter_ := getattr(self.node, "iter", None):
            return NodeWithOffset(iter_)
        if items := getattr(self.node, "items", None):
            # with statements
            last_item = items[-1]
            if v := last_item.optional_vars:
                return NodeWithOffset(v)
            return NodeWithOffset(last_item.context_expr)
        return NodeWithOffset(self.node)

    @property
    def lineno(self) -> int:
        return self._start_node().lineno

    @property
    def col_offset(self) -> int:
        return self._start_node().col_offset

    @property
    def end_lineno(self) -> int | None:
        return self._end_node().end_lineno

    @property
    def end_col_offset(self) -> int | None:
        return self._end_node().end_col_offset

    @classmethod
    def from_source(cls, source: str) -> NodeWalk:
        return cls(parse(source))

    @classmethod
    def from_file(cls, path: PathLike | str) -> NodeWalk:
        path = Path(path)
        return cls.from_source(path.read_text())
