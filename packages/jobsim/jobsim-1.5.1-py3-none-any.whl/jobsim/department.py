"""
Module docs
"""
import logging
import pathlib
import yaml
from typing import Dict
from dataclasses import dataclass
from dacite import from_dict
from jobsim import JOBSIM_PATH

LOGGER = logging.getLogger("Location")


@dataclass
class Depar:
    logo: str
    trainings: Dict[str, str]


class Department:
    def __init__(self, name, path=None):
        self.name = name
        self.info = self.get_department_info(path)

    def get_department_info(self, path):
        if path is None:
            file_path = JOBSIM_PATH / "departments" / f"{self.name}.yaml"
            with open(file_path, "r") as info:
                try:
                    dict_format = yaml.safe_load(info)
                except yaml.YAMLError:
                    LOGGER.error(f"yaml format of {file_path} is incorrect")
                    raise
            return from_dict(data_class=Depar, data=dict_format)
