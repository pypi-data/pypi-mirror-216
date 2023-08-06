"""
Module docs
"""
import logging
import pathlib
import yaml
from typing import Dict, List
from dataclasses import dataclass
from dacite import from_dict
from jobsim import JOBSIM_PATH

LOGGER = logging.getLogger("Location")


@dataclass
class Room:
    name: str
    availability: Dict[str, str]
    capacity: int


@dataclass
class _Location:
    flag: str
    rooms: List[Room]


class Location:
    def __init__(self, name, path=None):
        self.name = name
        self.info = self.get_location_info(path)

    def get_location_info(self, path):
        if path is None:
            file_path = JOBSIM_PATH / "locations" / f"{self.name.lower()}.yaml"
            with open(file_path, "r") as info:
                try:
                    dict_format = yaml.safe_load(info)
                except yaml.YAMLError:
                    LOGGER.error(f"yaml format of {file_path} is incorrect")
                    raise
            return from_dict(data_class=_Location, data=dict_format)

    def __hash__(self):
        return hash(self.name)
