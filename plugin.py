from LSP.plugin import AbstractPlugin
from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import Optional, List
import sublime


from os.path import join
from os.path import exists


def _flow_bin_path(path: str) -> str:
    return join(path, "node_modules", ".bin", "flow")


def _flow_config_path(path: str) -> str:
    return join(path, ".flowconfig")


class Flow(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def can_start(cls, _: sublime.Window, __: sublime.View,
        folders: List[WorkspaceFolder], configuration: ClientConfig
    ) -> Optional[str]:
        if not folders:
            return "need a folder"
        path = folders[0].path
        if not exists(_flow_config_path(path)):
            return "no .flowconfig present in {}".format(path)
        binpath = _flow_bin_path(path)
        if not exists(_flow_bin_path(path)):
            return "no flow binary found (tried: {})".format(binpath)
        configuration.command = [binpath, "lsp"]
        return None
