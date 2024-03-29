import time


def get_assignments_from_file(file_name: str) -> list[list]:
    with open(file_name, "r") as f:
        assignments = f.readlines()

    return [parse_assignment(assignment.strip()) for assignment in assignments]

def parse_assignment(assignment: str) -> list[tuple[set,set]]:
    assignments = assignment.split(",")

    def get_range_set(assignment_range: str) -> set:
        bounds = assignment_range.split("-")
        return set(range(int(bounds[0]),int(bounds[1])+1))

    return get_range_set(assignments[0]), get_range_set(assignments[1])

def ranges_encompass_one_another(ranges: tuple[set, set]) -> int:
    return int(ranges[0] <= ranges[1] or ranges[1] <= ranges[0])

def ranges_overlap(ranges: tuple[set, set]) -> int:
    return int(len(ranges[0] & ranges[1]) > 0)

start = time.time()
# Sample 1 - 2
print(sum([ranges_encompass_one_another(assignment) for assignment in get_assignments_from_file("sample_input.txt")]))

# Part 1 - 595
print(sum([ranges_encompass_one_another(assignment) for assignment in get_assignments_from_file("input.txt")]))

# Sample 2 - 4
print(sum([ranges_overlap(assignment) for assignment in get_assignments_from_file("sample_input.txt")]))

# Part 2 - 952
print(sum([ranges_overlap(assignment) for assignment in get_assignments_from_file("input.txt")]))

print(f"Finished in {time.time() - start} seconds") # Finished in 0.00921773910522461 seconds
