import shutil
import subprocess
from pathlib import Path


def shell_main(*args):
    # Get the path to the checker directory
    checker_dir = Path(__file__).resolve().parent
    # Get the checker type and arguments
    checker_type = args[0]
    checker_args = args[1:]

    # Run the appropriate checker tool with the specified arguments
    if checker_type == "shell":
        subprocess.run([f"{checker_dir}/test.bash", "-init"], cwd=".")
        shutil.copy(f"{checker_dir}/test.bash", "./test/test.bash")
    else:
        print(f"Unknown checker type: {checker_type}")
