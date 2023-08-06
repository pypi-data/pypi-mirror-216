import glob
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import List

import requests
import typer
import yaml
import yaspin
from termcolor import colored
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from cerebrium import FineTuner
from cerebrium import __version__ as cerebrium_version

app = typer.Typer()
env = os.getenv("ENV", "prod")

dashboard_url = (
    "https://dashboard.cerebrium.ai"
    if env == "prod"
    else "https://dev-dashboard.cerebrium.ai"
)
api_url = (
    "https://dev-rest-api.cerebrium.ai"
    if env == "dev"
    else "https://rest-api.cerebrium.ai"
)


@app.command()
def version():
    """
    Print the version of the Cerebrium CLI
    """
    print(cerebrium_version)


@app.command()
def login(
    private_api_key: str = typer.Argument(
        ...,
        help="Private API key for the user. Sets the environment variable CEREBRIUM_API_KEY.",
    )
):
    """
    Set private API key for the user in ~/.cerebrium/config.yaml
    """
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    config = (
        None
        if not os.path.exists(config_path)
        else yaml.full_load(open(config_path, "r"))
    )
    if config is None:
        config = {"api_key": private_api_key}
    else:
        config["api_key"] = private_api_key
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    print("✅  Logged in successfully.")


def get_api_key():
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    if not os.path.exists(config_path):
        print(
            "Please login using 'cerebrium login <private_api_key>' or specify the API key using the --api-key flag."
        )
        sys.exit(1)
    config = yaml.full_load(open(config_path, "r"))
    if config is None or "api_key" not in config:
        print(
            "Please login using 'cerebrium login <private_api_key>' or specify the API key using the --api-key flag."
        )
        sys.exit(1)
    return config["api_key"]


@app.command()
def deploy(
    name: str = typer.Argument(..., help="Name of the builder deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    hardware: str = typer.Option(
        "GPU",
        help="Hardware to use for the builder deployment. Can be one of 'CPU', 'GPU' or 'A10'.",
    ),
    include: List[str] = typer.Option(
        ["./*"], help="List of relative paths to files/folder to include."
    ),
    exclude: List[str] = typer.Option(
        ["./.*"],  # ignore .git etc. by default
        help="List of relative paths to files/folder to exclude.",
    ),
    init_debug: bool = typer.Option(
        False,
        help="Stops the container after initialization.",
    ),
    pre_init_debug: bool = typer.Option(
        False,
        help="Stops the container before initialization.",
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the builder deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
):
    """
    Deploy a builder deployment to Cerebrium
    """
    print(f"Deploying {name} with {hardware} hardware to Cerebrium...")
    if not api_key:
        api_key = get_api_key()

    requirements_hash = "REQUIREMENTS_FILE_DOESNT_EXIST"
    pkglist_hash = "PKGLIST_FILE_DOESNT_EXIST"

    # Check if main.py exists
    if not os.path.exists("./main.py"):
        print("main.py not found in current directory. This file is required.")
        sys.exit(1)

    # Check main.py for a predict function
    with open("./main.py", "r") as f:
        main_py = f.read()
        if "def predict(" not in main_py:
            print(
                "main.py does not contain a predict function. This function is required."
            )
            sys.exit(1)

    # Calc MD5 hash of ./requirements.txt
    if os.path.exists("./requirements.txt"):
        with open("./requirements.txt", "rb") as f:
            requirements_hash = hashlib.md5(f.read()).hexdigest()

    # Calc MD5 hash of ./pkglist.txt if it exists
    if os.path.exists("./pkglist.txt"):
        with open("./pkglist.txt", "rb") as f:
            pkglist_hash = hashlib.md5(f.read()).hexdigest()

    # Hit the deploy endpoint to get the upload URL
    upload_url_response = requests.post(
        f"{api_url}/deploy",
        headers={"Authorization": api_key},
        json={
            "name": name,
            "hardware": hardware.upper(),
            "init_debug": init_debug,
            "pre_init_debug": pre_init_debug,
            "log_level": log_level.upper(),
            "cerebrium_version": cerebrium_version,
            "requirements_hash": requirements_hash,
            "pkglist_hash": pkglist_hash,
        },
    )

    if upload_url_response.status_code != 200 or (
        upload_url_response.json().get("uploadUrl", None) is None
    ):
        print("API request failed with status code:", upload_url_response.status_code)
        print("Error getting upload URL:", upload_url_response.text)
        upload_url_response.raise_for_status()

    upload_url = upload_url_response.json()["uploadUrl"]
    project_id = upload_url_response.json()["projectId"]
    zip_file_name = upload_url_response.json()["keyName"]
    endpoint = upload_url_response.json()["internalEndpoint"]
    build_id = upload_url_response.json()["buildId"]

    print(f"Build ID: {build_id}")

    # Zip all files in the current directory and upload to S3
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        dir_name = os.path.dirname(zip_path)
        os.makedirs(dir_name, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            # check if each in include is a "[list, of, patterns]" and break up
            include = [i for pattern in include for i in pattern.strip("[]").split(",")]
            exclude = [e for pattern in exclude for e in pattern.strip("[]").split(",")]

            # Redundant include for the important files
            include.extend(
                x
                for x in [
                    "main.py",
                    "requirements.txt",
                    "pkglist.txt",
                    "conda_pkglist.txt",
                ]
                if x not in include
            )
            file_list = []
            for pattern in include:
                for file in glob.glob(pattern):
                    if (file not in file_list) and os.path.isfile(file):
                        file_list.append(Path(file).as_posix())

            # exclude files
            exclude_list = []
            for pattern in exclude:
                for file in glob.glob(pattern):
                    exclude_list.append(Path(file).as_posix())

            file_list = list(set(file_list) - set(exclude_list))
            print(f"Selected files: {file_list}")

            print("Zipping files...")
            for f in file_list:
                if os.path.isfile(f):
                    zip_file.write(f)

        print("⬆️  Uploading to Cerebrium...")
        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            with tqdm(
                total=os.path.getsize(zip_path),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                colour="#EB3A6F",
            ) as pbar:  # type: ignore
                wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=wrapped_f,  # type: ignore
                    timeout=60,
                    stream=True,
                )
            if upload_response.status_code != 200:
                print(
                    "API request failed with status code:", upload_response.status_code
                )
                print("Error uploading to Cerebrium:", upload_response.text)
                sys.exit(1)
            else:
                print("✅ Resources uploaded successfully.")

    # Poll the streamBuildLogs endpoint with yaspin for max of 10 minutes to get the build status
    t1 = time.time()
    seen_index = 0
    with yaspin.yaspin(text="🔨 Building...", color="yellow") as spinner:
        build_status = "IN_PROGRESS"
        while build_status != "success":
            build_status_response = requests.get(
                f"{api_url}/streamBuildLogs",
                params={"buildId": build_id},
                headers={"Authorization": api_key},
            )
            if build_status_response.status_code != 200:
                print(
                    "API request failed with status code:",
                    build_status_response.status_code,
                )
                print("Error getting build status:", build_status_response.text)
                sys.exit(1)
            else:
                build_status = build_status_response.json()["status"]
                response_logs = build_status_response.json()["logs"]
                if response_logs:
                    concat_logs = "".join(response_logs)
                    logs = concat_logs.split("\n")[:-1]
                else:
                    continue

                for message in logs[seen_index:]:
                    if message:
                        match = re.match(
                            r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                        )
                        if (
                            match is not None
                        ):  # If the regex matches the beginning of the string
                            created = match.group(
                                1
                            )  # The first group is the creation time
                            message = message[len(created) + 2 :]
                        spinner.write(f"{message}")
                    else:
                        spinner.write("\n")
                seen_index = len(logs)
                spinner.text = f"🔨 Building... Status: {build_status}"
                time.sleep(1)
            if time.time() - t1 > 600:
                spinner.fail("⏲️ Build timed out.")
                sys.exit(1)
            elif build_status == "build_failure" or build_status == "init_failure":
                spinner.fail("❌ Build failed.")
                sys.exit(1)
        spinner.text = f"Status: {build_status}"
        spinner.ok("🚀 Build complete!")
        print("\n🌍 Endpoint:", endpoint, "\n")
        print("💡 You can call the endpoint with the following curl command:")
        print(
            colored(
                f"curl -X POST {endpoint} \\\n"
                "     -H 'Content-Type: application/json' \\\n"
                "     -H 'Authorization: <public_api_key>' \\\n"
                "     --data '{}'",
                "green",
            )
        )
        print("----------------------------------------")
        print(
            f"🔗 View builds: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=builds"
        )
        print(
            f"🔗 View runs: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=runs"
        )


@app.command()
def delete_model(
    name: str = typer.Argument(..., help="Name of the builder deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
):
    if not api_key:
        api_key = get_api_key()
    print(f'Deleting model "{name}" from Cerebrium...')
    delete_response = requests.delete(
        f"{api_url}/delete-model",
        headers={"Authorization": api_key},
        json={
            "name": name,
        },
    )
    if delete_response.status_code != 200:
        print("API request failed with status code:", delete_response.status_code)
        print("Error deleting model:", delete_response.text)
        delete_response.raise_for_status()

    if delete_response.json()["success"]:
        print("✅ Model deleted successfully.")
    else:
        print("❌ Model deletion failed.")


@app.command()
def get_training_logs(
    job_id: str = typer.Argument(
        ..., help="Job ID returned for your training instance."
    ),
    api_key: str = typer.Option("", help="Private API key for the user."),
    polling_duration: int = typer.Argument(
        6000, help="Number of seconds to poll the training. Maximum of 15min."
    ),
):
    print(f"Retrieving training logs for {job_id}...")
    if not api_key:
        api_key = get_api_key()

    interval = 5  # seconds between polling.
    polling_duration = min(polling_duration, 60 * 15)

    # Poll the trainingLogs and make the output pretty
    seen_index = 0
    t_start = time.time()
    with yaspin.yaspin(text="CHECKING...", color="green") as spinner:
        train_status = "CHECKING..."
        while train_status != "succeeded":
            train_status_response = requests.post(
                f"{api_url}/job-logs",
                headers={"Authorization": api_key},
                json={"jobId": job_id},
            )

            if train_status_response.status_code != 200:
                print(
                    "API request failed with status code:",
                    train_status_response.status_code,
                )
                spinner.fail(
                    f"❌ Error fetching training job logs: {train_status_response.text}"
                )
                train_status_response.raise_for_status()
                sys.exit(1)
            else:
                train_status = train_status_response.json()["status"]
                if train_status == "pending":
                    spinner.text = f"🏋️ Training... Status: {train_status}"
                    time.sleep(interval)
                    continue

                response_logs = train_status_response.json().get("trainingLogs", None)
                if response_logs:
                    concat_logs = "".join(response_logs)
                    logs = concat_logs.split("\n")[:-1]
                else:
                    continue

                for message in logs[seen_index:]:
                    if message:
                        match = re.match(
                            r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                        )
                        if (
                            match is not None
                        ):  # If the regex matches the beginning of the string
                            created = match.group(
                                1
                            )  # The first group is the creation time
                            message = message[len(created) + 2 :]
                        spinner.write(f"{message}")
                    else:
                        spinner.write("\n")

                seen_index = len(logs)
                spinner.text = f"🏋️ Training... Status: {train_status}"
                time.sleep(interval)
            if time.time() - t_start > polling_duration:
                spinner.fail("⏲️ Training polling timed out.")
                sys.exit(1)
            elif train_status == "failed":
                spinner.fail("❌ Training failed.")
                sys.exit(1)
        spinner.ok("🚀 Training complete!")


@app.command()
def get_training_jobs(
    api_key: str = typer.Option("", help="Private API key for the user."),
    last_n: int = typer.Option(
        0, help="Number of last training jobs to fetch. Defaults to all"
    ),
):
    print("Getting status of recent training jobs...")
    if not api_key:
        api_key = get_api_key()
    status_response = requests.post(
        f"{api_url}/jobs",
        # f"{api_url}/training-jobs",
        headers={"Authorization": api_key},
        json={},
    )

    if status_response.status_code != 200:
        print("API request failed with status code:", status_response.status_code)
        print("Error: ", status_response.text)
        status_response.raise_for_status()

    trainingJobArr = status_response.json()["trainingJobArr"]

    if last_n > 0:
        trainingJobArr = trainingJobArr[:last_n]  # get the last n jobs

    # make the printing pretty using panels and boxes using rich. Not for MVP
    if len(trainingJobArr):
        print(
            f"\n{'-' * 60}\n✅Found the following training jobs:\n{'-' * 60}\n{'=' * 60}"
        )
        for trainingJob in trainingJobArr:
            print(
                f"🏋️ Training ID : {trainingJob['id']} 🏋️",
                f"*Job Name*: {trainingJob['name']}",
                f"*Project ID*: {trainingJob['projectId']}",
                f"*Created at*: {trainingJob['createdAt']}",
                f"*Status*: {trainingJob['status']}",
                f"{'=' * 60}",
                sep="\n",
            )
    else:
        print(
            "❌ Found no training jobs"
        )  # redundant catch in case.


@app.command()
def train(
    name: str = typer.Argument(..., help="Name for your training instance."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    hf_model_path: str = typer.Argument(..., help="Huggingface model path to use."),
    local_dataset_path: str = typer.Argument(
        ..., help="Path to your local dataset JSON file."
    ),
    training_args: str = typer.Option("", help="Json training arguments for the model. Example: '{\"num_train_epochs\": 5, \"learning_rate\": 1e-4}'"),
    hardware: str = typer.Option(
        "A10",
        help="Hardware to use for the builder deployment. Can be one of 'CPU', 'GPU' or 'A10'. !!! NOT IN USE !!!",
    ),
    model_type: str = typer.Option(
        "AutoModelForCausalLM",
        help="Huggingface model type used to load in pretrained weights.",
    ),
    init_debug: bool = typer.Option(
        False,
        help="Stops the container after initialization.",
    ),
    pre_init_debug: bool = typer.Option(
        False,
        help="Stops the container before initialization.",
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the builder deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
):
    """
    Deploy a fine tuning to Cerebrium
    """
    print(f"Fine tuning {name} with {hardware} hardware to Cerebrium...")
    if not api_key:
        api_key = get_api_key()
    # Creating the training object

    user_training_args = json.loads(training_args) if training_args else {}

    finetuning = FineTuner(
        experiment_name=name,
        hf_model_path=hf_model_path,
        dataset_path=local_dataset_path,
        model_type=model_type,
        api_key=api_key,
        training_kwargs=user_training_args,
    )
    finetuning._upload(
        init_debug=init_debug, pre_init_debug=pre_init_debug, log_level=log_level
    )


@app.command()
def download_model(
    job_id: str = typer.Argument(..., help="Job ID of your trained model."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    download_path: str = typer.Option(
        "",
        help="Path to download the model to. If not specified, the URL to model will be returned.",
    ),
):
    """
    Return a download link for the model.
    """
    print(f"Downloading model {job_id} from Cerebrium...")
    if not api_key:
        api_key = get_api_key()

    url_response = requests.post(
        f"{api_url}/download-model",
        json={"jobId": job_id},
        headers={"Authorization": api_key},
    )
    if url_response.status_code != 200:
        print(
            "API request failed with status code:",
            url_response.status_code,
        )
        print("Error downloading model:", url_response.text)
        url_response.raise_for_status()
    else:
        model_url = url_response.json()["message"]
        if download_path:
            print(f"Downloading model to {download_path}...")
            download_response = requests.get(
                model_url,
                timeout=60,
                stream=True,
            )

            with open(download_path, "wb") as f:
                with tqdm(
                    total=len(download_response.content),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:
                    for chunk in download_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                    if download_response.status_code != 200:
                        print(
                            "API request failed with status code:",
                            download_response.status_code,
                        )
                        print("Error downloading model:", download_response.text)
                        download_response.raise_for_status()
                    else:
                        print(f"Download complete. Saved to {download_path}.")
        else:
            print(f"Model download URL: {model_url}")


if __name__ == "__main__":
    app()
