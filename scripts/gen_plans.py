#!/usr/bin/env python3
"""Generate plans for all instance-1.pddl files in the ipc-2023 folder."""

import subprocess
import sys
from pathlib import Path

IPC_2023 = Path(__file__).parent / "ipc-2023" / "domains"


def main():
    instance_files = sorted(IPC_2023.rglob("instances/instance-1.pddl"))
    if not instance_files:
        print("No instance-1.pddl files found.")
        sys.exit(1)

    print(f"Found {len(instance_files)} instance(s).\n")

    for instance in instance_files:
        instances_dir = instance.parent  # .../instances/
        plans_dir = instances_dir / "plans"
        plans_dir.mkdir(exist_ok=True)

        cmd = [
            "up",
            "oneshot-planning",
            "--pddl",
            "../domain.pddl",
            "instance-1.pddl",
            "--plan",
            "plans/instance-1.plan",
        ]

        domain_name = instances_dir.parent.name
        print(f"[{domain_name}] Running: {' '.join(cmd)}  (cwd={instances_dir})")

        result = subprocess.run(cmd, cwd=instances_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[{domain_name}] OK -> {plans_dir / 'instance-1.plan'}")
        else:
            print(f"[{domain_name}] FAILED (exit {result.returncode})")
            if result.stderr:
                print(f"  stderr: {result.stderr.strip()}")
        print()


if __name__ == "__main__":
    main()
