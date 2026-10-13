from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PluginStartError
from LSP.plugin import WorkspaceFolder
from os.path import dirname
from os.path import exists
from os.path import join
import sublime


def _flow_bin_path(path: str) -> str:
    binfile = "flow.cmd" if sublime.platform() == "windows" else "flow"
    return join(path, "node_modules", ".bin", binfile)


def _flow_config_path(path: str) -> str:
    return join(path, ".flowconfig")


def _find_flow_root_path(directory: str) -> str | None:
    if exists(_flow_config_path(directory)):
        return directory
    elif directory == dirname(directory):
        return None
    else:
        return _find_flow_root_path(dirname(directory))


def plugin_loaded() -> None:
    Flow.register()


def plugin_unloaded() -> None:
    Flow.unregister()


class Flow(LspPlugin):
    @classmethod
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        file_path = context.view.file_name()
        path = _find_flow_root_path(dirname(file_path)) if file_path else None

        if not path:
            raise PluginStartError("no .flowconfig found in project or parent directories")

        binpath = _flow_bin_path(path)
        if not exists(binpath):
            raise PluginStartError("no flow binary found (tried: {})".format(binpath))

        context.workspace_folders.clear()
        context.workspace_folders.append(WorkspaceFolder.from_path(path))
        context.configuration.command = [binpath, "lsp"]
