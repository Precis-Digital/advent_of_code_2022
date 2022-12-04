from shared import utils


def extract_structured_assignments(assignment: str) -> tuple[range, range]:
    elfs = assignment.split(",")
    elf1, elf2 = list(list(map(int, elf.split("-"))) for elf in elfs)
    return range(elf1[0], elf1[1] + 1), range(elf2[0], elf2[1] + 1)


def fully_contains(container: range, containee: range, /) -> bool:
    return containee[0] in container and containee[-1] in container


def either_section_fully_contains(range1: range, range2: range, /) -> bool:
    return fully_contains(range1, range2) or fully_contains(range2, range1)


def find_overlap(range1: range, range2: range, /) -> range:
    return range(max(range1.start, range2.start), min(range1.stop, range2.stop))


def sections_overlap(range1: range, range2: range, /) -> bool:
    return bool(len(find_overlap(range1, range2)))


def main() -> None:
    assignments = utils.read_input_to_string().splitlines()
    fully_contains_count, overlap_count = 0, 0
    for assignment in assignments:
        sections1, sections2 = extract_structured_assignments(assignment=assignment)

        if either_section_fully_contains(sections1, sections2):
            fully_contains_count += 1

        if sections_overlap(sections1, sections2):
            overlap_count += 1

    print(f"Part 1: {fully_contains_count}")
    print(f"Part 2: {overlap_count}")


if __name__ == "__main__":
    main()
