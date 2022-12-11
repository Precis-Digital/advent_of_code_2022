from dataclasses import dataclass
import re
from typing import Optional
from collections import defaultdict
import uuid


COMMAND_MOVE_UP_LEVEL = "$ cd .."
COMMAND_LIST_FILES = "$ ls"
REGEX_CHANGE_DIRECTORY = r"\$ cd (.*)"

# regex for results from LS
REGEX_DIRECTORY = r"dir (.*)"
REGEX_FILE = r"(\d+) (.*)"


@dataclass
class Folder:
    directory_name: str
    files: list[tuple[int, str]]
    folders: list["Folder"]
    uid: str = None
    parent: "Folder" = None



    def create_folder(self, folder_name: str) -> "Folder":

        folder = Folder(directory_name=folder_name, files=[], folders=[], uid=uuid.uuid4().hex, parent=self)
        self.folders.append(folder)
        return folder

    def create_file(self, file_name: str, file_size: int) -> None:
        self.files.append((file_size, file_name))


    def get_folder(self, folder_name: str) -> Optional["Folder"]:
        for folder in self.folders:
            if folder.directory_name == folder_name:
                return folder
        return None

    def ls(self) -> list:
        for file in self.files:
            print(f"{file[0]} {file[1]}")
        for folder in self.folders:
            print(f"dir {folder.directory_name}")


def build_directory(fname: str) -> Folder:
    root_folder = None
    current_folder = None
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if line == COMMAND_MOVE_UP_LEVEL:
                current_folder = current_folder.parent
            elif line == COMMAND_LIST_FILES:
                pass
            elif match := re.match(REGEX_CHANGE_DIRECTORY, line):
                if match.group(1) == "/":
                    root_folder = Folder("/", [], [], uid=uuid.uuid4().hex)
                    current_folder = root_folder
                else:
                    new_folder = current_folder.get_folder(folder_name=match.group(1))
                    if new_folder is None:
                        raise ValueError(f"Folder {match.group(1)} not found in {current_folder.directory_name}")
                    current_folder = new_folder
            elif match := re.match(REGEX_DIRECTORY, line):
                current_folder.create_folder(match.group(1))
            elif match := re.match(REGEX_FILE, line):
                current_folder.create_file(match.group(2), int(match.group(1)))
            else:
                raise ValueError(f"Unexpected line: {line}")
    return root_folder


def get_folder_sums(folder: Folder) -> dict[str, int]:
    """
    recursively get the sum of all files in a folder
    :param folder:
    :return:
    """
    folder_sums = defaultdict(int)

    unvisited_folders = [folder]

    while unvisited_folders:
        current_folder = unvisited_folders.pop()
        sum_of_files = sum([file[0] for file in current_folder.files])

        # pdn = current_folder.parent.directory_name if current_folder.parent else None
        # print(current_folder.directory_name, current_folder.uid, sum_of_files, pdn, [f.directory_name for f in current_folder.folders])
        folder_sums[current_folder.uid] += sum_of_files
        parent = current_folder.parent
        while parent:
            folder_sums[parent.uid] += sum_of_files
            parent = parent.parent
        unvisited_folders.extend(current_folder.folders)

    return folder_sums

def solution1(root_folder: Folder) -> int:
    return sum([v for v in get_folder_sums(root_folder).values() if v <= 100000])

def solution2(root_folder: Folder) -> int:
    disk_space = 70000000
    root_folder_uid = root_folder.uid
    folder_sums = get_folder_sums(root_folder)
    root_folder_size = folder_sums[root_folder_uid]
    available_space = disk_space - root_folder_size
    space_needed = 30000000
    space_to_delete = space_needed - available_space

    return min([(v,k) for k,v in folder_sums.items() if v >= space_to_delete])

if __name__ == "__main__":
    SAMPLE_INPUT = "inputs/day-7-sample.txt"
    INPUT = "inputs/day-7-input.txt"

    root_folder = build_directory(INPUT)
    print(root_folder)
    print('s1', solution1(root_folder=root_folder)) # 1315285
    print('s2', solution2(root_folder=root_folder)) # 9847279

    # print(root_folder.files)
    # print(root_folder.ls())
    # print("A")
    # print(root_folder.get_folder("a").get_folder("e").ls())
    # print(get_folder_sums(folder=root_folder))
