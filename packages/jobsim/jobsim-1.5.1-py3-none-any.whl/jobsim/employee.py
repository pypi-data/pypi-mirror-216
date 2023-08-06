"""
Module docs
"""
import logging
from typing import Dict

LOGGER = logging.getLogger("Employee")


class Employee:
    def __init__(self, name, _id, department, location):
        self.name = name
        self._id = _id
        self.department = department
        self.location = location
        self.scheduled_trainings = {}
        self.finished_onboarding = False
        self.print_welcome_message()

    def get_name(self):
        return self.name

    def get_nick(self):
        if self.name == "John":
            return "Johnny"
        return self.name

    def print_welcome_message(self):
        print(
            f"{self.name} is a new employee in {self.location.name} {self.location.info.flag}"
        )
        print(
            f"{self.name} is joining {self.department.name.upper()} department {self.department.info.logo}"
        )

    @staticmethod
    def get_employee_code(employee_data: Dict):
        value = employee_data["departament_id"]
        if value < 0:
            raise ValueError("Wrong departament_id value It should be > 0")
        elif value > 25:
            return 100
        return 50

    def finish_onboarding(self):
        self.finished_onboarding = True

    def __str__(self):
        return (
            "Name: "
            + self.name
            + "\nID number: "
            + self._id
            + "\nDepartment: "
            + self.department
        )
