from pathlib import Path
from typing import Optional

from unified_planning.shortcuts import AbstractProblem

from tyr.problems.model import AbstractDomain, ProblemInstance


class IpcAbstractDomain(AbstractDomain):
    """
    Represents the base class for all IPC domains.
    """

    folder: Path

    @property
    def suffix(self) -> str:
        instance = next(self.instances_folder.iterdir())
        return instance.suffix

    @property
    def instances_folder(self) -> Path:
        return self.folder / "instances"

    def get_domain_path(self, problem_id: int) -> Path:
        if (self.folder / f"domain{self.suffix}").exists():
            return self.folder / f"domain{self.suffix}"
        return self.folder / "domains" / f"domain-{problem_id}{self.suffix}"

    def get_num_problems(self) -> int:
        return len(list(self.instances_folder.iterdir()))

    def build_problem_base(self, problem: ProblemInstance) -> Optional[AbstractProblem]:
        return self.load_from_files(
            self.instances_folder / f"instance-{problem.uid}{self.suffix}",
            self.get_domain_path(problem.uid),
        )


for ipc in Path(__file__).parent.iterdir():
    if ipc.is_dir() and "ipc" in ipc.name:
        for dom in (ipc / "domains").iterdir():
            if dom.is_dir():
                name = (ipc.name.capitalize() + dom.name.title() + "Domain").replace(
                    "-", ""
                )
                globals()[name] = type(
                    name,
                    (IpcAbstractDomain,),
                    {"folder": dom},
                )
