"""v2 plugin loader — incomplete, only loads markdown plugin."""

import importlib
import os


class PluginLoader:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def discover(self):
        """Find and load all plugins in the plugin directory."""
        if not os.path.isdir(self.plugin_dir):
            return

        for fname in os.listdir(self.plugin_dir):
            if fname.endswith("_plugin.py"):
                name = fname[:-3]
                # TODO: proper plugin loading with sandboxing
                spec = importlib.util.spec_from_file_location(
                    name, os.path.join(self.plugin_dir, fname)
                )
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "register"):
                    self.plugins[name] = mod.register()

    def get_plugin(self, name: str):
        return self.plugins.get(name)

    def render_with_plugins(self, content: str) -> str:
        """Apply all plugins to content — only markdown plugin exists."""
        for plugin in self.plugins.values():
            if hasattr(plugin, "transform"):
                content = plugin.transform(content)
        return content
