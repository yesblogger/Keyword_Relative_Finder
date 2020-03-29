import requests
from data import get_api
from datetime import date
import csv


# Global Variables

SEARCH_API = get_api()

DATASET = {}  # keyword value pair

IDENTIFIER = input("Please enter the seed Keyword: ").strip()

LOCATION = input("Please enter location for Google: ").strip()

# Functions


def writer_func(keyword, d=DATASET):
    filename = f"related_keywords_for_{keyword}_{date.today().__str__()}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as w_file:
        header = ["#", "Keywords"]
        writer = csv.DictWriter(w_file, fieldnames=header)
        writer.writeheader()
        for i, k in enumerate(DATASET.keys()):
            writer.writerow({"#": i, "Keywords": k})


def main():
    global IDENTIFIER
    relative_keyword_finder(IDENTIFIER)
    writer_func(IDENTIFIER)


def relative_keyword_finder(keyword, max_try=1):
    global IDENTIFIER, LOCATION, SEARCH_API
    if max_try > 100:
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
            if IDENTIFIER in query:
                try:
                    # condition when key in the dictionary
                    if not DATASET[query]:
                        DATASET[query] = 1
                        max_try += 1
                        relative_keyword_finder(query, max_try)
                except:
                    # condition when key is not in the dictionary
                    DATASET[query] = 0
    except:
        print("Response Error")


if __name__ == "__main__":
    main()
