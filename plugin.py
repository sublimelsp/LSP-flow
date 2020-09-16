from LSP.plugin import AbstractPlugin
from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import Optional, List
import os
import sublime


def _flow_bin_path(path: str) -> str:
    return os.path.join(path, "node_modules", ".bin", "flow")


def _flow_config_path(path: str) -> str:
    return os.path.join(path, ".flowconfig")


def _all_requirements_met(wf: WorkspaceFolder) -> bool:
    return os.path.exists(_flow_config_path(wf.path)) and \
           os.path.exists(_flow_bin_path(wf.path))


class Flow(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def can_start(
        cls,
        _: sublime.Window,
        __: sublime.View,
        folders: List[WorkspaceFolder],
        configuration: ClientConfig,
    ) -> Optional[str]:
        if not folders:
            return "need a folder"
        for i, wf in enumerate(folders):
            if _all_requirements_met(wf):

                # Swap the elements in the array so that the folder with the
                # .flowconfig file is at the front. This ensures that once we
                # construct the rootPath for the initialize request, the
                # rootPath is the one with the .flowconfig file. Otherwise,
                # flow crashes.
                folders[0], folders[i] = folders[i], folders[0]

                # Construct the startup command just in time.
                binpath = _flow_bin_path(folders[0].path)
                configuration.command = [binpath, "lsp"]

                # OK, let's start flow
                return None

        return "no .flowconfig found"
