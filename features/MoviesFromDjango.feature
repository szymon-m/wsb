Feature: Tworzymy plik zbior filmow z aktualnej bazy django

  # Enter feature description here



  Scenario: Generuje listę filmow z bazy django na potrzeby tabeli Films/Genres
    Given Mając baze django movie_db
    When Pobieram dane z bazy - helpers.from_django.retrieve_from_django(movie_db)
    Then Mam listę filmow

  Scenario: Zapisuje liste filmow z bazy django do pliku movies_django.csv
    Given Majac liste filmow
    When Kiedy zapisuje je do pliku .csv - helpers.from_django.create_movies_django_csv(movie_list)
    Then Otrzymuje plik movies_django.csv