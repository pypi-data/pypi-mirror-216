import hashlib
import json
import os
import sys
import tempfile
import zipfile
from copy import copy

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from transformers import (
    TrainingArguments,
)

from cerebrium import __version__
from cerebrium.requests import _cerebrium_request
from .finetuning_model import FineTuningModel
from .userDataset.base_dataset import FineTuningDataset


class FineTuner:
    def __init__(
        self,
        api_key: str,
        experiment_name: str,
        hf_model_path: str,
        dataset_path: str,
        model_type: str = "AutoModelForCausalLM",
        custom_tokenizer: str = "",
        base_model_kwargs: dict = {},
        peft_lora_kwargs: dict = {},
        training_kwargs: dict = {},
        dataset_kwargs: dict = {},
        seed: int = 42,
        verbose=False,
    ):
        """An object for finetuning transformers on Cerebrium to improve the perfromance of Large Language Models towards your task.


        Args:
            experiment_name (str): The unique name you would like to use to refer to your training. Will be used as the model name for deploying to cerebrium.
            hf_model_path (str): The path to the model on huggingface.
            dataset_path (str): Path of your local dataset.json file.
            model_type (str, optional): Type of model to use. Defaults to "AutoModelForCausalLM".
            custom_tokenizer (str, optional): If you need something other than "AutoTokenizer for your model. Defaults to "".
            base_model_kwargs (dict, optional): Any kwargs you need to send to from_pretrained(). Defaults to {}.
            peft_lora_kwargs (dict, optional): Kwargs to be fed into LoraConfig(), eg. lora rank. Defaults to {}.
            training_kwargs (dict, optional): Any custom training args you have. Defaults to {}.
            dataset_kwargs (dict, optional): Additional kwargs to be parsed into the FineTuningDataset. Defaults to {}.
            seed (int, optional): Pytorch seed. Defaults to 42.
            verbose (bool, optional): _description_. Defaults to False.
        """

        self.name = experiment_name
        self.api_key = api_key
        self.seed = seed
        self.verbose = verbose
        self.dataset_path = dataset_path
        self.hf_model_path = hf_model_path
        self.user_base_model_kwargs = copy(base_model_kwargs)
        self.user_peft_kwargs = copy(peft_lora_kwargs)

        # will set to our defaults. Easier for beginners.
        # Calling here so that a user can access the defaults and check them before training.
        self.user_training_kwargs = training_kwargs

        self.finetuning_model = FineTuningModel(
            hf_base_model_path=hf_model_path,
            model_type=model_type,
            base_model_kwargs=base_model_kwargs,
            lora_kwargs=peft_lora_kwargs,
            verbose=self.verbose,
        )
        self.custom_tokenizer = custom_tokenizer
        if (
            str.find(self.hf_model_path, "llama") != -1
        ):  # if llama model, use llama tokenizer. This seems to have broken in the latest huggingface release
            self.custom_tokenizer = "LlamaTokenizer"

        self.dataset = FineTuningDataset(
            dataset_path=dataset_path, verbose=self.verbose, **dataset_kwargs
        )

    def TrainingArguments(self, training_kwargs: dict = {}) -> TrainingArguments:
        """A utility function to create training arguments for user inspection.
        A set of default training arguments is used if none are provided

        Args:
            logging_steps (int, optional): Steps between logging. Defaults to 10.
            per_device_batch_size (int, optional): Batch size. Defaults to 15.
            warmup_steps (int, optional): Warmup before beginning training. Defaults to 50.
            micro_batch_size (int, optional): Defaults to 4.
            num_epochs (int, optional): Number of epochs to train for. Defaults to 3.
            learning_rate (float, optional): Initial learning rate. Defaults to 3e-4.
            group_by_length (bool, optional): Defaults to False.


        Returns:
            TrainingArguments: _description_
        """

        defaults = {
            "logging_steps": 10,
            "per_device_train_batch_size": 15,
            "per_device_eval_batch_size": 15,
            "warmup_steps": 0,
            "gradient_accumulation_steps": 4,
            "num_train_epochs": 3,
            "learning_rate": 1e-4,
            "group_by_length": False,
            "output_dir": "./",
        }

        for k, v in defaults.items():
            if k not in training_kwargs:
                training_kwargs[k] = v

        return TrainingArguments(
            **training_kwargs,
        )

    def create_json_config(self, filename="finetune.json"):
        # Quick json serialiser. Dumps all the variables as a config
        config_dict = self.__dict__.copy()
        config_dict["finetuning_model"] = config_dict["finetuning_model"].to_dict()
        config_dict["dataset"] = config_dict["dataset"].to_dict()

        with open(filename, "w") as f:
            json.dump(config_dict, fp=f, indent=2, sort_keys=True)

    def _upload(self, init_debug=False, pre_init_debug=False, log_level="INFO"):
        dataset_hash = "DATASET_FILE_DOESNT_EXIST"

        # Calc MD5 hash of user's dataset
        assert os.path.exists(
            self.dataset_path
        ), "Dataset file cannot be found. Please check the path you have entered!"
        with open(self.dataset_path, "rb") as f:
            dataset_hash = hashlib.md5(f.read()).hexdigest()
        # Hit the deploy endpoint to get the upload URL
        upload_url_response = _cerebrium_request(
            method="train",
            http_method="POST",
            api_key=self.api_key,
            payload={
                "name": self.name,
                "hf_model_path": self.hf_model_path,
                "hardware": "A10",
                "init_debug": init_debug,
                "pre_init_debug": pre_init_debug,
                "log_level": log_level,
                "cerebrium_version": __version__,
                "dataset_hash": dataset_hash,
            },
        )
        if upload_url_response["status_code"] != 200 or (
            upload_url_response["data"].get("uploadUrl", None) is None
        ):
            print(
                "API request failed with status code:",
                upload_url_response["status_code"],
            )
            print("Error getting upload URL:", upload_url_response["data"]["message"])
            sys.exit(1)
        upload_url = upload_url_response["data"]["uploadUrl"]
        job_id = upload_url_response["data"]["jobId"]

        print(f"Job ID: {job_id}")
        # Zip all files in the current directory and upload to S3
        print("Zipping files...")
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, f"{self.name}.zip")
            dir_name = os.path.dirname(zip_path)
            os.makedirs(dir_name, exist_ok=True)
            # Create a zip file containing the config files and upload them.
            with zipfile.ZipFile(
                os.path.join(temp_dir, f"{self.name}.zip"), "w"
            ) as zip:
                self.create_json_config("finetune_config.json")
                zip.write("finetune_config.json")
                zip.write(self.dataset_path, "dataset.json")

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
                        "API request failed with status code:",
                        upload_response.status_code,
                    )
                    print("Error uploading to Cerebrium:", upload_response.text)
                    raise Exception("Error uploading to Cerebrium")
                else:
                    print(f"✅ Resources uploaded successfully for {job_id}.")
            print(
                "You can query the training status with `cerebrium get-training-jobs <API_KEY>` \n",
                "Your training logs can be found at `cerebrium get-training-logs <JOB_ID> <API_KEY>` ",
            )
