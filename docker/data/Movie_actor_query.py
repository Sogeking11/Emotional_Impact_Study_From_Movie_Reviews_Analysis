import requests
import api_keys  # Assuming you have a separate Python file containing the TMDB API key as 'TMDB'
import json

# Function to get the movie IDs for a given actor
def get_movie_ids(actor_name):
    base_url = "https://api.themoviedb.org/3/search/person"
    api_key = api_keys.TMDB
    movie_ids = []

    try:
        response = requests.get(base_url, params={"api_key": api_key, "query": actor_name})
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            actor_id = data["results"][0]["id"]
            credits_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
            response_credits = requests.get(credits_url, params={"api_key": api_key})
            response_credits.raise_for_status()
            credits_data = response_credits.json()
            if credits_data.get("cast"):
                movie_ids = [movie["id"] for movie in credits_data["cast"]]
        else:
            print(f"Actor '{actor_name}' not found.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    return movie_ids

# List of actor names
actor_names = ['Samuel L Jackson', 'Tom Cruise', 'Brad pitt', 'Will Smith', 'Johnny Depp', 'Charlton Heston', 'Clint Eastwood', 'Harrison Ford', 'Jack Nicholson', 'Halle Berry', 'Meryl Streep', 'Scarlett Johansson', 'Jennifer Lawrence', 'Julia Roberts', 'Uma Thurman', 'Sigourney Weaver', 'Sandra Bullock', 'Marion Cotillard', 'Ellen Page', 'Nicolas Cage']

# Loop through all actors and get all the movies IDs
all_movie_ids = []
for actor_name in actor_names:
    movie_ids = get_movie_ids(actor_name)
    all_movie_ids.extend(movie_ids)
    print(f"Found {len(movie_ids)} movies for actor '{actor_name}'.")
print(f"Found {len(all_movie_ids)} movies in total.")
# store in a dictionary with "id" as key and "movie_ids" as value
all_movie_ids = {"id": all_movie_ids}
# write the list of movie ids to a json file
with open('movie_ids.json', 'w') as f:
    json.dump(all_movie_ids, f)
