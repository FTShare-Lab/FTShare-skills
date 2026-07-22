from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from urllib.parse import urlparse

import pytest


ROOT = Path(__file__).resolve().parent
HANDLERS = sorted(ROOT.glob("sub-skills/*/scripts/handler.py"))


def _load_handler(path: Path):
    name = "contract_" + path.parents[1].name.replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _argument_flags(path: Path) -> set[str]:
    flags = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "add_argument":
            continue
        flags.update(
            arg.value
            for arg in node.args
            if isinstance(arg, ast.Constant)
            and isinstance(arg.value, str)
            and arg.value.startswith("--")
        )
    return flags


def _route_literals(path: Path) -> set[str]:
    routes = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        value = node.value
        start = value.find("api/v1/")
        if start < 0:
            continue
        route = "/" + value[start:].split("?", 1)[0]
        if route != "/api/v1/":
            routes.add(route.rstrip("/"))
    return routes


def _frontmatter_name(path: Path) -> str | None:
    skill = path.parents[1] / "SKILL.md"
    if not skill.exists():
        return None
    for line in skill.read_text(encoding="utf-8").splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None


@pytest.mark.parametrize("handler", HANDLERS, ids=lambda path: path.parents[1].name)
def test_every_handler_has_valid_skill_contract(handler):
    tree = ast.parse(handler.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "main" in functions
    assert _frontmatter_name(handler) == handler.parents[1].name
    assert _route_literals(handler), "handler must contain a public /api/v1 route"
    source = handler.read_text(encoding="utf-8")
    for flag in _argument_flags(handler):
        dest = flag[2:].replace("-", "_")
        assert dest in source, f"{flag} is declared but never referenced"


@pytest.mark.parametrize("handler", HANDLERS, ids=lambda path: path.parents[1].name)
def test_every_handler_cli_flag_is_statically_discoverable(handler):
    flags = _argument_flags(handler)
    for flag in flags:
        assert flag.startswith("--")
        assert " " not in flag


def test_handler_inventory_and_cli_surface_are_fully_enumerated():
    assert len(HANDLERS) == 153
    flags = {flag for handler in HANDLERS for flag in _argument_flags(handler)}
    assert len(flags) == 96
    assert sum(len(_argument_flags(handler)) for handler in HANDLERS) == 491


@pytest.mark.parametrize("handler", HANDLERS, ids=lambda path: path.parents[1].name)
def test_safe_urlopen_rejects_cross_origin_requests(handler, monkeypatch):
    module = _load_handler(handler)
    safe_urlopen = getattr(module, "safe_urlopen", None)
    if safe_urlopen is None:
        pytest.skip("legacy handler has no safe_urlopen wrapper")

    base_url = getattr(module, "BASE_URL", None)
    if base_url is None and hasattr(module, "base_url"):
        base_url = module.base_url()
    assert base_url
    parsed = urlparse(base_url)
    foreign = f"{parsed.scheme}://example.invalid/api/v1/market/data/test"

    opened = False

    def fail_open(*args, **kwargs):
        nonlocal opened
        opened = True
        raise AssertionError("cross-origin request reached opener")

    opener = getattr(module, "SAFE_URLOPENER", None)
    if opener is not None:
        monkeypatch.setattr(opener, "open", fail_open)

    with pytest.raises(SystemExit):
        safe_urlopen(foreign)
    assert not opened
