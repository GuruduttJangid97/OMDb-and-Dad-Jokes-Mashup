import requests_with_caching

apikey = ""  # you may *optionally* replace this with your API key.
requests_with_caching.clear_cache()
# print(list(requests_with_caching.perm_cache().keys()))

def get_movie_data(name: str) -> dict:
    base_url = "http://www.omdbapi.com/"
    params = {"t": name, "r": "json"}
    title = requests_with_caching.get(base_url, params=params, permanent_cache_file="./assets/permanent_cache.txt")
    return title.json()


def rt_rating(movie_data: dict) -> int:
    data = movie_data["Ratings"][1]["Value"]
    return int(data.strip('%'))

def get_joke_data(jokes: str)-> dict:
    joke_url = "https://icanhazdadjoke.com/search"
    params = {"limit": 2, "term": jokes}
    headers = {"Accept": "application/json"}

    data = requests_with_caching.get(joke_url ,headers=headers, params=params, permanent_cache_file="./assets/permanent_cache.txt")
    return data.json()

def get_jokes(plot: str, verbosity=0) -> tuple[str, list[str]]:
    words = plot.split()  # split into separate words
    words = [w.strip(",.!;:") for w in words]  # remove punctuation for each word

    # WRITE YOUR CODE HERE
    words = sorted(words, key=len, reverse=True)
    for word in words:
        Joke_Data = get_joke_data(word)
        if Joke_Data["results"]:
            joke = []
            for result in Joke_Data["results"]:
                joke.append(result["joke"])
            return (word, joke)
    return (None, None)

def highlight(word: str, sentence: str) -> str:
    import re

    # Escape special characters in the word to treat it as a literal string
    # Use re.sub() to replace the word with the highlighted version
    # Use re.IGNORECASE flag to perform case-insensitive replacement
    return re.sub(re.escape(word), f"**{word}**", sentence, flags=re.IGNORECASE)


def haha_me(movie_title: str, verbosity=0) -> str:
    movie_data = get_movie_data(movie_title)
    
    if movie_data is None:
        return "No movie found: " + movie_title

    movie_name = movie_data["Title"]
    
    rotten_tomatoes = rt_rating(movie_data)
    
    movie_plot = movie_data["Plot"]

    joke, jokes = get_jokes(movie_plot, verbosity)
    if joke is None:
        return "I've got no jokes about this movie. It's too serious!"

    plot = highlight(joke, movie_plot)

    if rotten_tomatoes == -1:
        joke_message = "Hope you like them!"
    elif rotten_tomatoes < 70:
        joke_message = "Hope they're better than the movie!"
    else:
        joke_message = "Hope they're as good as the movie!"

    highlighted_jokes = [highlight(joke, j) for j in jokes]

    return "\n".join([
        movie_name,
        f"Rotten Tomatoes rating: {rotten_tomatoes}%",
        plot,
        f"Speaking of **{joke}**, that reminds me of some jokes.",
        joke_message,
        "",
        "\n".join(highlighted_jokes),
    ])

print(haha_me("Venom"))