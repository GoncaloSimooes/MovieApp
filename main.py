from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    storage_json = StorageJson('movies.json')
    storage_csv = StorageCsv('movies.csv')
    storage = storage_json
    movie_app = MovieApp(storage)
    movie_app.title()
    movie_app.run()


if __name__ == "__main__":
    main()
