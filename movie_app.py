import statistics
import random
from fuzzywuzzy import fuzz
from colorama import Fore, Style


class MovieApp:
    def __init__(self, storage):
        """
        Initializes a MovieApp instance.
        Args:
        storage: An object implementing the storage interface for movie data.
        """
        self.storage = storage

    def title(self):
        """
        Displays the title of the movie application.
        """
        print(Fore.GREEN + """********** My Movies Database **********""" + Style.RESET_ALL + "\n")

    def run(self):
        """
        Runs the main loop of the movie application, displaying the menu and processing user input.
        """
        print(Fore.YELLOW + """ Menu:
    0. Exit   
    1. List movies
    2. Add movie
    3. Delete movie
    4. Stats
    5. Random movie
    6. Search movie
    7. Movies sorted by rating
    8. Generate website""" + Style.RESET_ALL)
        print("   ")

        option = int(input(Fore.CYAN + "Enter choice (0-8): " + Style.RESET_ALL))
        print("   ")

        if option == int(0):
            self.exit_menu()

        elif option == int(1):
            self.storage.list_movies()

        elif option == int(2):
            title_movie = input("Enter movie title: ")
            self.storage.add_movie(title_movie)

        elif option == int(3):
            title_movie = input("Enter movie name to delete: ")
            self.storage.delete_movie(title_movie)

        elif option == int(4):
            self.stats_movies()

        elif option == int(5):
            self.random_movies()

        elif option == int(6):
            self.search_movies()

        elif option == int(7):
            self.sorted_movies()

        elif option == int(8):
            self.generate_website()

        else:
            self.run()
            print(" Invalid option  ")

        self.press_enter_continue()
        print("   ")

    def press_enter_continue(self):
        """
        Prompts the user to press Enter to continue and waits for user input.
        """
        input(Fore.CYAN + "Press enter to continue" + Style.RESET_ALL)
        return self.run()

    def exit_menu(self):
        """
        Exits the movie application.
        """
        print("Bye!")
        return exit()

    def stats_movies(self):
        """
        Displays statistics about the movies in the database, such as average and median rating,
        as well as the best and worst rated movies.
        """
        movies = self.storage.load_movies()
        ratings = []
        for movie in movies:
            rating_str = movie.get("rating", "0.0")
            if rating_str.replace(".", "").isdigit():
                ratings.append(float(rating_str))
            else:
                ratings.append(0.0)

        average_rating = statistics.mean(ratings)
        print(Fore.CYAN + f"Average rating: {round(average_rating, 3)}" + Style.RESET_ALL)

        median_rating = statistics.median(ratings)
        print(Fore.CYAN + f"Median rating: {median_rating}" + Style.RESET_ALL)

        best_rating = 0.0
        worst_rating = 10.0
        best_movie = ""
        worst_movie = ""
        for movie in movies:
            rating_str = movie.get("rating", "0.0")
            if rating_str.replace(".", "").isdigit():
                rating = float(rating_str)
                if rating > best_rating:
                    best_rating = rating
                    best_movie = movie["title"]
                if rating < worst_rating:
                    worst_rating = rating
                    worst_movie = movie["title"]

        print(Fore.CYAN + f"Best Movie: {best_movie}, {best_rating}" + Style.RESET_ALL)
        print(Fore.CYAN + f"Worst Movie: {worst_movie}, {worst_rating}" + Style.RESET_ALL)

    def random_movies(self):
        """
        Picks a random movie from the database and displays its title and rating.
        """
        movies = self.storage.load_movies()
        movie = random.choice(movies)
        print(Fore.CYAN + f"Your movie for tonight: {movie['title']}, it's rated {movie['rating']}" + Style.RESET_ALL)

    def search_movies(self):
        """
        Searches for movies in the database that match a given search name and displays the results.
        """
        movies = self.storage.load_movies()
        search_name = input(Fore.CYAN + "Enter part of movie name: " + Style.RESET_ALL).lower()
        matching_movies = []
        for movie in movies:
            if fuzz.token_sort_ratio(search_name, movie["title"].lower()) >= 50:
                matching_movies.append(movie)
        if len(matching_movies) > 0:
            print(f"Found {len(matching_movies)} movies:")
            for movie in matching_movies:
                print(movie["title"], movie["rating"])
        else:
            print("No movies found.")

    def sorted_movies(self):
        """
        Displays the movies in the database sorted by rating in descending order.
        """
        movies = self.storage.load_movies()
        for movie in movies:
            rating_str = movie.get("rating", "0.0")
            if not rating_str.replace(".", "").isdigit():
                rating_str = "0.0"
            movie["rating"] = float(rating_str)
        sorted_movies_list = sorted(movies, key=lambda x: x["rating"], reverse=True)
        for movie in sorted_movies_list:
            print(movie["title"], movie["rating"])

    def generate_website(self):
        """
        Generates a website with information about the movies in the database,
        using a template file and movie data.
        """
        with open("_static/index_template.html", 'r') as f:
            template_content = f.read()

        all_movies = self.storage.load_movies()

        movies_info = ""
        for movie in all_movies:
            title = movie.get('title')
            year = movie.get('year')
            rating = movie.get("rating")
            poster_url = movie.get('poster_url')
            imdb_id = movie.get('imdb_ID')
            movie_info = f'''
            <div>
                <ol class='movie-grid'>
                    <li>
                        <div class='movie'>
                            <a href='https://www.imdb.com/title/{imdb_id}' target='_blank'>
                                <img class='movie-poster' src='{poster_url}'/>
                            </a>
                            <div class='movie-title'>{title}</div>
                            <div class='movie-year'>{year}</div>
                            <div class='movie-rating'>{rating} IMDb</div>
                        </div>
                    </li>
                </ol>
            </div>'''

            movies_info += movie_info

        html_content = template_content.replace('__TEMPLATE_MOVIE_GRID__', movies_info)

        with open("_static/index.html", "w") as f:
            f.write(html_content)

        print("Website was generated successfully.")

