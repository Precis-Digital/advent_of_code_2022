from shared import utils


def main() -> None:
    data = utils.read_input_to_string()
    elf_sums = sorted(
        (
            sum(int(calories) for calories in elf.split("\n"))
            for elf in data.split("\n\n")
        )
    )

    print(f"Part 1: {elf_sums[-1]}")
    print(f"Part 2: {sum(elf_sums[-3:])}")


if __name__ == "__main__":
    main()
