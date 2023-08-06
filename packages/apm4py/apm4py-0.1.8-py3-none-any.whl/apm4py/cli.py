import glob
import json
import os
from pathlib import Path
import sys
import typer
from typing import Optional

import apm4py

app = typer.Typer()


@app.command()
def upload(
    data_folder: str = typer.Argument(help="Folder where data sets are stored"),
    name: Optional[str] = typer.Option(None, help="Name of the event log"),
    profile: str = typer.Option("default", help="Profile of the Process Mining host"),
):
    apm_dir = os.path.join(os.environ.get("HOME"), ".apm")
    apm_profile_path = os.path.join(os.environ.get("HOME"), ".apm", profile)
    if not os.path.exists(apm_profile_path):
        if not os.path.exists(apm_dir):
            os.mkdir(apm_dir)

        print(f"Profile {profile} does not exists. Please create a profile first.")
        profile = typer.prompt("Name of your profile", default="default")
        if profile == "":
            profile = "default"

        host = typer.prompt("Hostname")
        scheme = typer.prompt("Scheme", default="https")
        port = typer.prompt("Port", default="auto")
        token = typer.prompt("API Token", default="None")

        profile_config = {"host": host, "scheme": scheme}

        if port != "auto":
            profile_config["port"] = port

        if token != "None":
            profile_config["token"] = token

        apm_profile_path = os.path.join(os.environ.get("HOME"), ".apm", profile)
        with open(apm_profile_path, "w") as profile_file:
            json.dump(profile_config, profile_file)

    else:
        with open(apm_profile_path, "r") as profile_file:
            profile_config = json.loads(profile_file.read())

    api = apm4py.create_api(**profile_config)
    event_file = get_file_by_pattern(data_folder, "*[eE]vent*.csv")
    event_semantics = get_file_by_pattern(data_folder, "*[eE]vent*.json")
    case_file = get_file_by_pattern(data_folder, "*[cC]ase*.csv")
    case_semantics = get_file_by_pattern(data_folder, "*[cC]ase*.json")

    name = name if name is not None else Path(event_file).stem
    api.upload_event_log_file(
        name=name,
        event_file_path=event_file,
        event_semantics_path=event_semantics,
        case_file_path=case_file,
        case_semantics_path=case_semantics,
    )


def get_file_by_pattern(dir: str, file_pattern: str) -> Optional[str]:
    files = glob.glob(os.path.join(dir, file_pattern))
    if len(files) == 0:
        return None

    if len(files) > 1:
        raise (f"There should be only 1 file matching '{file_pattern}'")

    return files[0]


def main():
    sys.exit(app())


if __name__ == "__main__":
    main()
