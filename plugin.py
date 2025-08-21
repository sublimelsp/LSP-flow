from LSP.plugin import AbstractPlugin
from LSP.plugin import ClientConfig
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import Optional, List
import sublime


from os.path import dirname, exists, join


def _flow_bin_path(path: str) -> str:
    binfile = "flow.cmd" if sublime.platform() == "windows" else "flow"
    return join(path, "node_modules", ".bin", binfile)


def _flow_config_path(path: str) -> str:
    return join(path, ".flowconfig")


def _find_flow_root_path(directory: str) -> Optional[str]:
    if exists(_flow_config_path(directory)):
        return directory
    elif directory == dirname(directory):
        return None
    else:
        return _find_flow_root_path(dirname(directory))


def plugin_loaded() -> None:
    register_plugin(Flow)


def plugin_unloaded() -> None:
    unregister_plugin(Flow)


class Flow(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def can_start(
        cls,
        _: sublime.Window,
        initiating_view: sublime.View,
        folders: List[WorkspaceFolder],
        configuration: ClientConfig,
    ) -> Optional[str]:
        path = _find_flow_root_path(dirname(initiating_view.file_name()))

        if not path:
            return "no .flowconfig found in project or parent directories"

        binpath = _flow_bin_path(path)
        if not exists(binpath):
            return "no flow binary found (tried: {})".format(binpath)

        folders.clear()
        folders.append(WorkspaceFolder.from_path(path))
        configuration.command = [binpath, "lsp"]
        return None
