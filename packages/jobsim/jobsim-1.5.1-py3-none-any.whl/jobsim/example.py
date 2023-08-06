from jobsim.employee import Employee
from jobsim.location import Location
from jobsim.department import Department
from jobsim.trainings_scheduler import schedule_trainings

IT = "it"
FINANCE = "finance"
SF = "San_francisco"
KRK = "Krakow"
SYD = "Sydney"

employee_1 = Employee("Jackie", "1", Department(IT), Location(SF))
employee_2 = Employee("Molly", "2", Department(FINANCE), Location(SF))
employee_3 = Employee("Mark", "3", Department(IT), Location(KRK))
employee_4 = Employee("John", "4", Department(IT), Location(SYD))
employee_5 = Employee("Bob", "5", Department(FINANCE), Location(SYD))
employee_6 = Employee("Andrew", "6", Department(FINANCE), Location(KRK))
employee_7 = Employee("Tom", "7", Department(FINANCE), Location(SYD))
employee_8 = Employee("Gary", "8", Department(IT), Location(SF))
employee_9 = Employee("Martin", "9", Department(IT), Location(SF))

schedule_trainings(
    [
        employee_1,
        employee_2,
        employee_3,
        employee_4,
        employee_5,
        employee_6,
        employee_7,
        employee_8,
        employee_9,
    ]
)
