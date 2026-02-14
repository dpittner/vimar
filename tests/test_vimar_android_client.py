import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "custom_components" / "vimar_viewapp" / "vimar_android_client.py"

# Stub package context and dependency to allow isolated unit testing without Home Assistant.
pkg = types.ModuleType("custom_components")
pkg.__path__ = []
sys.modules.setdefault("custom_components", pkg)
subpkg = types.ModuleType("custom_components.vimar_viewapp")
subpkg.__path__ = [str(ROOT / "custom_components" / "vimar_viewapp")]
sys.modules.setdefault("custom_components.vimar_viewapp", subpkg)

const_mod = types.ModuleType("custom_components.vimar_viewapp.const")
const_mod.VIMAR_PACKAGE = "it.vimar.View"
sys.modules.setdefault("custom_components.vimar_viewapp.const", const_mod)

u2 = types.ModuleType("uiautomator2")
u2.Device = object
u2.connect = lambda *args, **kwargs: None
sys.modules.setdefault("uiautomator2", u2)

spec = importlib.util.spec_from_file_location(
    "custom_components.vimar_viewapp.vimar_android_client", MODULE_PATH
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)
VimarAndroidClient = module.VimarAndroidClient


class TestVimarAndroidClientParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.client = VimarAndroidClient(
            adb_host="127.0.0.1",
            adb_port=5555,
            serial=None,
            username="u",
            password="p",
            pin=None,
        )

    def test_extract_shades_from_percent_labels(self):
        xml = '''
        <node text="Living Room"/>
        <node text="65%"/>
        <node text="Kitchen"/>
        <node text="10%"/>
        '''
        shades = self.client._extract_shades(xml)
        self.assertEqual(len(shades), 2)
        self.assertEqual(shades[0].name, "Living Room")
        self.assertEqual(shades[0].position, 65)
        self.assertEqual(shades[1].id, "kitchen")

    def test_extract_scenarios_deduplicates(self):
        xml = '''
        <node text="Scenario Morning"/>
        <node text="Scenario Morning"/>
        <node text="Scena Notte"/>
        <node text="Other"/>
        '''
        scenarios = self.client._extract_scenarios(xml)
        self.assertEqual({s.id for s in scenarios}, {"scenario_morning", "scena_notte"})


if __name__ == "__main__":
    unittest.main()
