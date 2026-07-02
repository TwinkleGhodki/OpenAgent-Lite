import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dispatcher.dispatcher import Dispatcher


def test_dispatcher_registers_and_lists_actions():
    dispatcher = Dispatcher()

    dispatcher.register("greet", lambda name: f"hi {name}")
    dispatcher.register("add", lambda a, b: a + b)

    assert dispatcher.list_actions() == ["add", "greet"]


def test_dispatcher_wraps_errors_for_failed_execution():
    dispatcher = Dispatcher()

    def fail():
        raise ValueError("boom")

    dispatcher.register("fail", fail)

    try:
        dispatcher.execute("fail")
    except RuntimeError as exc:
        assert "Execution failed for action 'fail'" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError for failing action")
