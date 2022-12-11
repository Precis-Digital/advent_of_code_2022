import importlib
import re
import time
import traceback
from functools import cache

import requests

SESSION_COOKIE_STRING_PATH = "secrets/session_cookie.txt"
BASE_URL = "https://adventofcode.com/"

@cache
def get_session_cookie() -> str:
    with open(SESSION_COOKIE_STRING_PATH, "r") as f:
        return f.readline()

def remove_leading_zero(num: str) -> str:
    """Returns a leading zero number as non leading zero"""
    if int(num[0]) == 0:
        return int(str(num)[1:])
    return int(num)

def add_leading_zero(num: str) -> str:
    """Returns a non-leading zero number as a leading zero number"""
    if int(num) < 10:
        return "0" + str(int(num))
    return str(num)

def get_input_file(day_num: str, year_num):
    # Input file
    url = f"{BASE_URL}{year_num}/day/{day_num}/input"
    resp = requests.get(url, cookies={"session": get_session_cookie()}, headers={'User-Agent': "jonas@precisdigital.com"})
    
    if "before it unlocks" in resp.text:
        raise Exception(f"That day is not ready yet... Please wait until 6AM CEST to start a new AOC day :)")
    
    if resp.status_code == 404:
        raise Exception(f"Could not find the puzzle input at ${url}")

    return resp.text

def generate_new_day(day_num: str, year_num: str = "2022"):
    folder_name = f"Dec{add_leading_zero(day_num)}"
    if os.path.exists(folder_name):
        raise Exception(f"The folder ./{folder_name} already exists. If you want to recreate that day please delete the folder first.")
    
    url = f"{BASE_URL}{year_num}/day/{day_num}"
    input_file = get_input_file(day_num, year_num)
    os.makedirs(folder_name)
    with open(f"{folder_name}/input.txt", "w") as f:
        f.write(input_file)

    with open(f"{folder_name}/sample_input.txt", "w") as f:
        f.write("Overwrite this file with values from the puzzle :)")
    
    with open(f"{folder_name}/__init__.py", "w") as f:
        f.write("")
    
    with open(f"{folder_name}/main.py", "w") as f:
        f.write(f"""
# Day {day_num}, Year {year_num}
# Link: {url}
def get_input_values(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return f.readlines()

def part_1_sample():
    input_values = get_input_values('{folder_name}/sample_input.txt')
    print('You need to write this function yourself :)')
    print('Dont forget to copy paste the sample input into the sample_input.txt file.')
    return len(input_values)

def part_1_answer():
    input_values = get_input_values('{folder_name}/input.txt')
    print('You need to write this function yourself :)')
    return len(input_values)

def part_2_sample():
    input_values = get_input_values('{folder_name}/sample_input.txt')
    print('You need to write this function yourself :)')
    print('Dont forget to copy paste the sample input into the sample_input.txt file.')
    return len(input_values)

def part_2_answer():
    input_values = get_input_values('{folder_name}/input.txt')
    print('You need to write this function yourself :)')
    return len(input_values)
        """)
    
    return url

def submit_answer(answer: str, level: str, day_num: str, year_num: str = "2022"):
    url = f"{BASE_URL}{year_num}/day/{day_num}"
    res = requests.post(url=url, data={"level": level, "answer": answer}, headers={'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': "jonas@precisdigital.com"}, cookies={"session": get_session_cookie()})

    rex = re.compile("<article[^>]*>(.*?)</article>", re.S|re.M)
    regex_match = rex.match(res.text)
    if regex_match:
        return regex_match.groups()[0].strip()
    
    if 'Both parts of this puzzle are complete' in res.text:
        return 'Both parts of this puzzle are already complete!'

    return res.text

def get_all_existing_folder_names():
    subfolders = [f.path[2:] for f in os.scandir() if f.is_dir() and len(f.path) == 7]
    return sorted(subfolders)

import os


def clear_console():
    os.system("clear")

def clear_console_and_print(string: str) -> None:
    clear_console()
    print(string)

def generate_new_day_prompt():
    while True:
        clear_console()
        resp = input("Input the day in numbers (fx. 8, 08, 10, 12): ")
        try:
            url = generate_new_day(add_leading_zero(remove_leading_zero(resp)))
            print("Generated new day folder for you!")
            print(f"You can visit the page for the that day here: {url}")
            time.sleep(1)
            break
        except Exception as e:
            clear_console_and_print(f"Could not generate a new day: {str(e)}")
            time.sleep(2)

def break_or_continue():
    res = input("Would you like to return to the menu and try again? Y/N ")
    if res.lower() == "y":
        return "continue"
    return "break"

def run_functions_prompt():
    folder_name = None
    while True:
        clear_console_and_print(f"The following days are set up in your folder:\n")
        for i, folder in enumerate(get_all_existing_folder_names(), 1): print(f"[{i}] {folder}")
        resp = input("Select a day by writing the number: ")
        if resp == "":
            return
        try:
            folder_name = get_all_existing_folder_names()[int(resp)-1]
            break
        except IndexError:
            print(f"Not a valid number - please try again.")
            time.sleep(1)
    
    day_num = folder_name.replace("Dec", "")
    date_module = importlib.import_module(f"{folder_name}.main")

    while True:
        clear_console_and_print(f"""
You're working with '{folder_name}'🎄.
What would you like to do next?🎅

[1] Run the 'part_1_sample' function?
[2] Run the 'part_1_answer' function?
[3] Run the 'part_2_sample' function?
[4] Run the 'part_2_answer' function?
        """)
        resp = input("Select an option by writing the number: ")
        clear_console()
        if str(resp) == "1":
            # Run sample function
            print("Running the sample function for part 1.🎄")
            try:
                print(20*"-")
                ans = date_module.part_1_sample()
                print(20*"-")
                print(f"The answer to the Part 1 sample function was calculated as '{ans}'.")
            except:
                print("An error occured while running the Part 1 sample function:")
                print(20*"-")
                traceback.print_exc()
                print(20*"-")

            if break_or_continue() == "continue": 
                continue
            else:
                break
        elif str(resp) == "2":
            # Run part 1 answer function
            print("Running the answer function for part 1.🎄")
            try:
                print(20*"-")
                ans = date_module.part_1_answer()
                print(20*"-")
                print(f"The answer to the Part 1 answer function was calculated as '{ans}'.")
                resp = input("Should I try to submit that for you? Y/N ")
                if resp.lower() == "y":
                    res = submit_answer(ans, 1, day_num)
                    print(f"AOC responded with: {res}" )
                    if break_or_continue() == "continue": 
                        continue
                    else:
                        break
            except:
                print("An error occured while running the Part 1 answer function:")
                print(20*"-")
                traceback.print_exc()
                print(20*"-")

        elif str(resp) == "3":
            # Run sample function
            print("Running the sample function for part 2.🎄")
            try:
                print(20*"-")
                ans = date_module.part_2_sample()
                print(20*"-")
                print(f"The answer to the Part 2 sample function was calculated as '{ans}'.")   
            except:
                print("An error occured while running the Part 2 sample function:")
                print(20*"-")
                traceback.print_exc()
                print(20*"-")

            if break_or_continue() == "continue": 
                continue
            else:
                break
        elif str(resp) == "4":
            # Run part 2 answer function
            print("Running the answer function for part 2.🎄")
            try:
                print(20*"-")
                ans = date_module.part_2_answer()
                print(20*"-")
                print(f"The answer to the Part 2 answer function was calculated as '{ans}'.")
                resp = input("Should I try to submit that for you? Y/N ")
                if resp.lower() == "y":
                    res = submit_answer(ans, 2, day_num)
                    print(f"AOC responded with: {res}" )
                    if break_or_continue() == "continue": 
                        continue
                    else:
                        break
            except:
                print("An error occured while running the Part 2 answer function:")
                print(20*"-")
                traceback.print_exc()
                print(20*"-")

        elif resp == "":
            break

        else:
            print(f"Unknown response '{resp}' - please try again.")
            time.sleep(1)

while True:
    clear_console_and_print(f"""
🎄Welcome to Jonas' AOC Utils!🎄
What do you want to do? 🎅

[1] Generate a new day
[2] Run functions from an existing day.
    """)
    resp = input("Select an option by writing the number: ")
    if str(resp) == "1":
        generate_new_day_prompt()
    elif str(resp) == "2":
        run_functions_prompt()
        break
