"""
agentkit.py — the shared deterministic harness for "The Agent Graph" course.

THE CONTRACT (every episode imports this; no downloads, no keys, no network):
  1. SEEDED MOCK LLM   — ScriptedLLM replays canned model turns in STRICT order,
                         so the agent is a pure function of (script, call-index).
  2. SCRIPTED TOOLS    — every tool is a pure function over an in-memory `world` dict.
  3. TRACE             — records every (kind, payload) step; figures are drawn FROM
                         this object, never from hand-typed numbers.
  4. THREE-WAY IDENTITY— assert_identity(figure, terminal, headline) proves the
                         white-card figure == the printed trace == the headline.
  5. REPRODUCE PROOF   — reproduce(run) runs twice and asserts byte-identical traces.

Only the model's *words* are ever fake. The loop/graph/state/tools are real code.
"""
from __future__ import annotations
import json, random, copy
from dataclasses import dataclass, field

SEED = 7
random.seed(SEED)  # any sampling/jitter is seeded; we never call a real provider.


# ── 1 · seeded mock LLM ───────────────────────────────────────────────────────
class ScriptedLLM:
    """Replays a hand-authored list of canned turns in strict order.

    A turn is a dict. For a ReAct loop:
      {"thought": "...", "action": "calc", "action_input": "12+30"}  # act
      {"thought": "...", "answer": "84"}                              # stop
    The model is a pure function of (script, call_index): identical inputs,
    identical outputs, forever. A turn that is deliberately *wrong* (bad action)
    followed by a corrected turn makes retry curves REAL, not faked.
    """
    def __init__(self, script: list[dict], name: str = "mock"):
        self.script = list(script)
        self.name = name
        self.i = 0

    def __call__(self, _prompt: str) -> dict:
        if self.i >= len(self.script):
            raise RuntimeError(f"ScriptedLLM[{self.name}] ran out of turns at call {self.i}")
        turn = copy.deepcopy(self.script[self.i])
        self.i += 1
        return turn

    def reset(self):
        self.i = 0


# ── 2 · scripted tool environment ────────────────────────────────────────────
class ToolError(Exception):
    pass


def make_world() -> dict:
    """A tiny seeded in-memory world. No filesystem, no HTTP. Pure data."""
    return {
        "calls": 0,
        "kb": {  # a canned 'search index'
            "remotion": "Remotion renders video with React.",
            "langgraph": "LangGraph models an agent as a directed graph.",
        },
    }


def tool_calc(world: dict, expr: str):
    """Deterministic calculator over a whitelisted arithmetic grammar."""
    world["calls"] += 1
    allowed = set("0123456789+-*/(). ")
    if not expr or set(expr) - allowed:
        raise ToolError(f"calc: illegal expression {expr!r}")
    return eval(expr, {"__builtins__": {}}, {})  # ponytail: input is whitelisted above


def tool_search(world: dict, query: str):
    world["calls"] += 1
    q = query.strip().lower()
    if q not in world["kb"]:
        raise ToolError(f"search: no entry for {query!r}")
    return world["kb"][q]


TOOLS = {"calc": tool_calc, "search": tool_search}


# ── 3 · trace ────────────────────────────────────────────────────────────────
@dataclass
class Trace:
    steps: list[dict] = field(default_factory=list)

    def add(self, kind: str, **payload):
        self.steps.append({"kind": kind, **payload})

    # figures read these — never hand-typed numbers.
    def count(self, kind: str) -> int:
        return sum(1 for s in self.steps if s["kind"] == kind)

    def tool_counts(self) -> dict:
        out: dict[str, int] = {}
        for s in self.steps:
            if s["kind"] == "action":
                out[s["tool"]] = out.get(s["tool"], 0) + 1
        return out

    def key(self) -> str:
        """Canonical serialization for the reproduce-to-the-digit proof."""
        return json.dumps(self.steps, sort_keys=True, default=str)

    def ladder(self) -> list[dict]:
        """Render-ready rungs for the Act-2 trace-ladder figure."""
        return self.steps


# ── 4 · three-way identity ───────────────────────────────────────────────────
def assert_identity(figure_value, terminal_value, headline_value):
    """The white-card figure, the printed trace, and the headline are ONE run."""
    assert figure_value == terminal_value == headline_value, (
        f"three-way identity broken: figure={figure_value!r} "
        f"terminal={terminal_value!r} headline={headline_value!r}"
    )
    return figure_value


# ── 5 · reproduce proof ──────────────────────────────────────────────────────
def reproduce(run) -> Trace:
    """Run the episode twice; assert byte-identical traces. Returns the trace."""
    a = run()
    b = run()
    assert a.key() == b.key(), "NOT reproducible: two runs produced different traces"
    return a


def dump(trace: Trace, path: str):
    """Persist the real trace so the Remotion figure is drawn from the same run."""
    with open(path, "w") as f:
        json.dump({"steps": trace.steps,
                   "tool_counts": trace.tool_counts()}, f, indent=2)
