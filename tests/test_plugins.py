import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dispatcher.dispatcher import Dispatcher
from plugins import discover_plugins
from plugins.base import Plugin


class DummyPlugin(Plugin):
    name = "dummy"
    description = "A dummy plugin"

    def execute(self, *args, **kwargs):
        return "done"


def test_dispatcher_registers_plugins():
    dispatcher = Dispatcher()
    dispatcher.register_plugin(DummyPlugin())

    assert dispatcher.execute("dummy") == "done"


def test_discover_plugins_finds_core_plugins():
    plugins = discover_plugins()
    names = {plugin.name for plugin in plugins}

    assert "open_youtube" in names
    assert "start_scheduler" in names
