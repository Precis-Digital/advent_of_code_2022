import requests

SESSION_COOKIE_STRING_PATH = "secrets/session_cookie.txt"
BASE_URL = "https://adventofcode.com/"

def get_session_cookie() -> str:
    with open(SESSION_COOKIE_STRING_PATH, "r") as f:
        return f.readline()

def generate_new_day(day_num: str, year_num: str = "2022"):
    # Input file
    resp = requests.get(f"{BASE_URL}/{year_num}/day/{day_num}/input")
    print(resp)


while True:
    print(f"""
Welcome to xmas_utils! What do you want to do
[1] Generate a new day
    """)
    resp = input("Select an option by writing the number: ")
    if str(resp) == "1":
        print("OK!")
    

    break
