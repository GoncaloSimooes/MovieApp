from istorage import IStorage
import json
import requests


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        The function loads the information from the JSON
        file and returns the data.
        """
        movies_list = self.load_movies()
        total_movies = len(movies_list)
        print(f"{total_movies} movies in total")
        for movie in movies_list:
            print(f"{movie['title']} ({movie['year']}), Rating: {movie['rating']}")

    def add_movie(self, title_movie):
        """
        Adds a movie to the movie database.
        Loads the information from the OMDB API, adds the movie,
        and saves it.
        """
        try:
            data = self.data_api(title_movie)
        except ValueError as e:
            print(str(e))
            return

        new_movie = {
            "title": data["Title"],
            "year": data["Year"],
            "rating": data["imdbRating"],
            "poster_url": data["Poster"],
            "imdb_ID": data["imdbID"]
        }

        movies_list = self.load_movies()
        movie_titles = [movie["title"] for movie in movies_list]
        if new_movie["title"] in movie_titles:
            print(f"Movie '{new_movie['title']}' already exists in the database.")
            return

        movies_list.append(new_movie)
        self.save_movies(movies_list)
        print(f"Movie '{new_movie['title']}' was added to the database.")

    def delete_movie(self, title_movie):
        """
        Deletes a movie from the movie database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies_list = self.load_movies()
        movie_titles = [movie["title"].strip().lower() for movie in movies_list]
        if title_movie.strip().lower() in movie_titles:
            for movie in movies_list:
                if movie["title"].strip().lower() == title_movie.strip().lower():
                    movies_list.remove(movie)
                    self.save_movies(movies_list)
                    print(f"Movie '{title_movie}' successfully deleted.")
                    break
        else:
            print(f"Movie '{title_movie}' doesn't exist in the database!")

    def load_movies(self):
        """Loads data from the JSON file and returns a list of dictionaries."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def data_api(self, title_movie):
        """Makes a request to the OMDB API and returns the JSON response."""
        api_request = "http://www.omdbapi.com/?apikey=1c26b87f"
        params = {'t': title_movie}
        response = requests.get(api_request, params)
        response_json = response.json()
        if response_json.get('Response') == 'False':
            raise ValueError(f"Could not find movie with title '{title_movie}'.")
        return response_json

    def save_movies(self, movies):
        """Saves the list of dictionaries in the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(movies, f)


storage = StorageJson('movies.json')