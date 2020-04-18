import requests
from data import get_api
from datetime import date
from location import geo_code
import csv


# Global Variables

SEARCH_API = get_api()

DATASET = {}  # keyword value pair

IDENTIFIER = []

LOCATION = ""

while True:
    if not len(LOCATION):
        LOCATION = geo_code(
            input("Please enter location for Google: ").strip())
    IDENTIFIER.append(input("Please enter a keyword: ").strip())
    resp = input(
        "Do you want to enter more keywords (y or n): ").lower().strip()
    if LOCATION != "" and resp == 'n':
        break

# Functions


def writer_func(d=DATASET):
    filename = f"related_keywords_for_{date.today().__str__()}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as w_file:
        header = ["#", "Keywords"]
        writer = csv.DictWriter(w_file, fieldnames=header)
        writer.writeheader()
        for i, k in enumerate(DATASET.keys()):
            writer.writerow({"#": i, "Keywords": k})


def matcher(q):
    for i in IDENTIFIER:
        if i not in q:
            return False
    return True


def main():
    global IDENTIFIER
    relative_keyword_finder(" ".join(IDENTIFIER))
    if len(DATASET):
        writer_func()


def relative_keyword_finder(keyword, max_try=1):
    global LOCATION, SEARCH_API
    if max_try > 1000:
        return None
    # Setting parameters for API call
    params = {
        'access_key': SEARCH_API,
        'query': keyword,
        "gl": LOCATION
    }

    # feting json content from the api
    api_response = requests.get(
        'http://api.serpstack.com/search', params=params).json()
    try:
        # related searches as list of dictionary
        for r_searches in api_response['related_searches']:
            query = r_searches['query'].strip()
            if matcher(query):
                try:
                    # action when key in the dictionary
                    DATASET[query]
                except:
                    # condition when key is not in the dictionary
                    DATASET[query] = 0
        # set condition to execute what will happen at the end of the above iteration
        key = list(DATASET.keys())[list(DATASET.values()).index(0)]
        DATASET[key] = 1
        max_try += 1
        relative_keyword_finder(key, max_try)
    except:
        print("Response Error or Max recursion depth reach or DATASET reached completion")


if __name__ == "__main__":
    main()
