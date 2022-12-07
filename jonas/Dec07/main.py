COMMAND_LINE_TYPE = "command"
PRINT_LINE_TYPE = "print"
CHANGE_DIRECTORY_COMMAND = "cd"
LIST_COMMAND = "ls"
DIR_PRINT_TYPE = "dir"
FILE_PRINT_TYPE = "file"

def read_command_line_input(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return [TerminalLine(line.strip()) for line in f.readlines()]


class TerminalLine:
    line_string: str

    def __init__(self, line_string: str) -> "TerminalLine":
        self.line_string = line_string

    @property
    def is_command(self) -> bool:
        return self.line_string[0] == "$"

    @property
    def command_arg(self) -> str:
        return self.line_string.split(" ")[2] if self.is_change_directory_command else None

    @property
    def is_change_directory_command(self) -> bool:
        return self.is_command and self.line_string.split(" ")[1] == CHANGE_DIRECTORY_COMMAND
    
    @property
    def is_list_command(self) -> bool:
        return self.is_command and self.line_string.split(" ")[1] == LIST_COMMAND
    
    @property
    def is_stdout_type(self) -> bool:
        return not self.is_command

    @property
    def is_stdout_dir_type(self) -> bool:
        return self.is_stdout_type and self.line_string.split(" ")[0] == DIR_PRINT_TYPE
    
    @property
    def is_stdout_file_type(self) -> bool:
        return self.is_stdout_type and not self.is_stdout_dir_type
    
    @property
    def printed_directory_name(self) -> str:
        return self.line_string.split(" ")[1] if self.is_stdout_dir_type else None
    
    @property
    def printed_file_name(self) -> str:
        return self.line_string.split(" ")[1] if self.is_stdout_file_type else None
    
    @property
    def printed_file_size(self) -> int:
        return int(self.line_string.split(" ")[0]) if self.is_stdout_file_type else None
    
    def __repr__(self) -> str:
        return self.line_string

class File:
    path: str
    size: int
    name: str

    def __init__(self, path: str, size: int, name: str) -> "File":
        self.path = path
        self.size = size
        self.name = name
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class Directory:
    path: str
    size: int
    name: str
    files: list[File]
    subdirectories: list[str]

    def __init__(self, path: str, name: str) -> "Directory":
        self.path = path
        self.name = name
        self.size = 0
        self.files = []
        self.subdirectories = []

    @property
    def direct_files_size(self):
        return sum([file.size for file in self.files])
    
    def calculate_subdirectory_size(self, all_directories_dict: dict[str, "Directory"]) -> int:
        self.size = self.direct_files_size
        for directory_pointer in self.subdirectories:
            subdirectory = all_directories_dict[directory_pointer]
                
            self.size += subdirectory.calculate_subdirectory_size(all_directories_dict)
        return self.size
    
    def __repr__(self) -> str:
        return str(self.__dict__)


def get_directory_dict_from_terminal_lines(lines: list[TerminalLine]) -> dict[str, Directory]:
    directory_dict: dict[str, Directory] = {}
    current_path = ""
    i = 0
    while i < len(lines):
        if lines[i].is_change_directory_command:
            if lines[i].command_arg == "..":
                # Moving up one
                current_path = ("/".join(current_path.split("/")[:-2])) + "/"
                i += 1
            else:
                # Moving down one
                current_path += lines[i].command_arg + "/"
                i += 1
            
            if current_path[:2] == "//":
                current_path = current_path[1:]

            if not directory_dict.get(current_path):
                directory_dict[current_path] = Directory(name=lines[i].command_arg, path = current_path)
            
        elif lines[i].is_list_command:
            i += 1

            # All PRINT_LINE_TYPES that comes after a LIST_COMMAND must be files or directories
            while i < len(lines) and lines[i].is_stdout_type:
                if lines[i].is_stdout_file_type:
                    directory_dict[current_path].files.append(File(path=f"{current_path}{lines[i].printed_file_name}", size=lines[i].printed_file_size, name=lines[i].printed_file_name))
                elif lines[i].is_stdout_dir_type:
                    directory_dict[current_path].subdirectories.append(f"{current_path}{lines[i].printed_directory_name}/")
        
                i += 1
                
    for key in directory_dict:
        directory_dict[key].calculate_subdirectory_size(directory_dict)

    return directory_dict

# Solution 1
def less_than_100000_directories(directory_dict: dict[str, Directory]) -> list[Directory]:
    filtered_list = []
    for directory in directory_dict.values():
        if directory.size < 100_000 and directory.path != "/":
            filtered_list.append(directory)
    
    return filtered_list

# Solution 2
def find_smallest_directory_greater_than_limit(directory_dict: dict[str, Directory]) -> list[Directory]:
    min_path = ""
    min_value = 0
    total_space = 70_000_000
    target_unused_space = 30_000_000
    currently_used_space = directory_dict["/"].size
    currently_unused_space = total_space - currently_used_space

    for directory in directory_dict.values():
        size_below_target = (currently_unused_space - target_unused_space) + directory.size
        if size_below_target < 0:
            continue

        if size_below_target < min_value or min_value == 0:
            min_value = size_below_target
            min_path = directory.path
    
    return directory_dict[min_path]


# Sample 1 - 95437
print(sum([directory.size for directory in less_than_100000_directories(get_directory_dict_from_terminal_lines(read_command_line_input("sample_input.txt")))]))

# Part 1 - 1644735
print(sum([directory.size for directory in less_than_100000_directories(get_directory_dict_from_terminal_lines(read_command_line_input("input.txt")))]))

# Sample 2 - 24933642
print(find_smallest_directory_greater_than_limit(get_directory_dict_from_terminal_lines(read_command_line_input("sample_input.txt"))).size)

# Part 2 - 1300850
print(find_smallest_directory_greater_than_limit(get_directory_dict_from_terminal_lines(read_command_line_input("input.txt"))).size)
