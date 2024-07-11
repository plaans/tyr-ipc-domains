from pathlib import Path

from tyr.problems.model import FolderAbstractDomain


for ipc in Path(__file__).parent.iterdir():
    if ipc.is_dir() and "ipc" in ipc.name:
        for dom in (ipc / "domains").iterdir():
            if dom.is_dir():
                name = (ipc.name.capitalize() + dom.name.title() + "Domain").replace(
                    "-", ""
                )
                globals()[name] = type(
                    name,
                    (FolderAbstractDomain,),
                    {"folder": dom},
                )
