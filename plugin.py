from LSP.plugin import AbstractPlugin
from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin import ResolvedStartupConfig
from LSP.plugin.core.typing import Optional, List
import sublime


from os import path as os_path
from os import pardir, sep


def _flow_bin_path(path: str) -> str:
    return os_path.join(path, "node_modules", ".bin", "flow")


def _flow_config_path(path: str) -> str:
    return os_path.join(path, ".flowconfig")


def _find_flow_root_path(starting_dir) -> str:
    # Find the flow binary closest to the current file,
    # searching up the directory structure
    # Setup initial directories
    last_dir = ""
    curr_dir = starting_dir
    # Loop through parent directories until you hit the end or find a match
    while last_dir != curr_dir:
        if os_path.exists(_flow_bin_path(curr_dir)):
            break
        last_dir = curr_dir
        curr_dir = os_path.abspath(curr_dir + os_path.sep + pardir)
    return curr_dir


class Flow(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def on_pre_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: List[WorkspaceFolder],
        resolved: ResolvedStartupConfig,
    ) -> Optional[str]:
        starting_dir, filename = os_path.split(initiating_view.file_name())
        path = _find_flow_root_path(starting_dir)
        binpath = _flow_bin_path(path)
        resolved.command = [binpath, "lsp"]
        workspace_folders = [
            WorkspaceFolder.from_path(os_path.join(path, "")),
        ]
        return path

    @classmethod
    def can_start(
        cls,
        _: sublime.Window,
        initiating_view: sublime.View,
        folders: List[WorkspaceFolder],
        configuration: ClientConfig,
    ) -> Optional[str]:
        starting_dir, filename = os_path.split(initiating_view.file_name())
        path = _find_flow_root_path(starting_dir)
        folders = [
            WorkspaceFolder.from_path(os_path.join(path, "")),
        ]
        if not os_path.exists(_flow_config_path(path)):
            return "no .flowconfig present in {}".format(path)
        binpath = _flow_bin_path(path)
        if not os_path.exists(_flow_bin_path(path)):
            return "no flow binary found (tried: {})".format(binpath)
        return None
