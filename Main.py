import requests_with_caching

apikey = ""  # you may *optionally* replace this with your API key.
requests_with_caching.clear_cache()
# print(list(requests_with_caching.perm_cache().keys()))

def get_movie_data(name: str) -> dict:
    base_url = "http://www.omdbapi.com/"
    params = {"t": name, "r": "json"}
    title = requests_with_caching.get(base_url, params=params, permanent_cache_file="./assets/permanent_cache.txt")
    return title.json()

result = get_movie_data("Black Panther")
print(result)