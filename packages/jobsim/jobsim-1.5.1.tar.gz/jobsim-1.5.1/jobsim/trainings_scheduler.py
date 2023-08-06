from collections import defaultdict


def schedule_trainings(employees):
    to_schedule = {}
    trainings = {}
    locations = {}

    print("\n----------------- Required trainings -----------------\n")
    for employee in employees:
        if employee.location not in to_schedule.keys():
            if employee.location.name not in to_schedule:
                to_schedule[employee.location.name] = defaultdict(int)
            locations[employee.location.name] = employee.location
        to_print = ""
        for training, duration in employee.department.info.trainings.items():
            trainings[training] = duration
            to_schedule[employee.location.name][training] += 1
            to_print += f"{training}, "
        print(f"Required trainings for {employee.name}: {to_print}")

    scheduled = {}
    for location, trs in to_schedule.items():
        scheduled[location] = {}
        for tr in sorted(trs, key=trainings.get, reverse=True):
            duration = int(trainings[tr].split("h")[0])
            capacity = trs[tr]
            for room in locations[location].info.rooms:
                if room.capacity >= capacity:
                    term = get_term(room.availability, duration)
                    if term:
                        scheduled[location][tr] = f"{room.name} {term}"

    print("\n----------------- Scheduled trainings -----------------\n")
    for employee in employees:
        for training in employee.department.info.trainings:
            if training in scheduled[employee.location.name]:
                employee.scheduled_trainings[training] = scheduled[
                    employee.location.name
                ][training]
        to_print = ""
        for tr, term in employee.scheduled_trainings.items():
            to_print += f"{tr} {term}, "
        print(f"Trainings for {employee.name}: {to_print}")


def get_term(availability, duration):
    result_day = None
    start_hour = None
    for day, hours in availability.items():
        start, end = hours.split("-")
        if duration <= int(end) - int(start):
            result_day = day
            start_hour = int(start)
            break
    if result_day:
        availability.pop(result_day)
        return f"{result_day} {start_hour}-{start_hour + duration}"
