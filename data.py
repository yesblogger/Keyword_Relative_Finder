def get_api():
    with open("search_api.txt", mode="r") as r_file:
        return r_file.readline().strip()
