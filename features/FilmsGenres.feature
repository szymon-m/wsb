Feature: Tabela pomocnicza Filmy i Gatunki

  Tworzy wazoną tablice gatunkow
  Jeżeli film jest w:
    1) dwóch gatunkach np. Drama i Comedy, wtedy wagi dzielone są przez liczbę gatunków czyli 2
       Drama : 0.5   Comedy : 0.5
    2) trzech gatunkach - dzielone przez liczbę stwierdzonych dla filmu gatunków tj. 3
       Drama : 0.333 Comedy : 0.3333 Horror: 0.3333

  Tabela będzie miała postać
  ======================================================================
  =         = Action = Drama  =  Horror  = Thriller =  Comedy = (COUNT_GENRES)
  ======================================================================
  =  film#1 =  0.5   =    0   =    0.5   =     0    =     0   =    2
  =  film#2 =   0    = 0.3333 =     0    =  0.3333  =  0.3333 =    3
  ======================================================================
  itd.

  Scenario: Przygotuj słownik gatunków z pliku movies.csv
    Given Posiadajac plik movies csv z filmami i gatunkami
    When kiedy uruchamiam funkcję helpers.genres.create_genres_dict(movies_file)
    Then funkcja zwraca słownik gatunków

  Scenario: Przygotuj naglowek tabeli z pliku movies.csv
    Given Majac plik movies.csv
    When kiedy uruchamiam funkcję helpers.genres.create_data_frame(movies_file)
    Then otrzymuję pusty pandas Datframe zawierajacy w naglowku wszystkie gatunki filmow

  Scenario: Wypelnij dataframe wartosciami 0 lub 1 w zaleznosci czy film nalezy do gatunku
    Given Posiadajac plik movies csv
    And listę id filmow wystepujacycj juz w bazie django
    When kiedy wywoluje funkcje helpers.genres.populate_dataframe(movies_file, django_movies_ids)
    Then otrzymuje wypelniona tabele filmow z 0 lub 1 w zaleznosci czy film nalezy do gatunku

  Scenario: films_genres.csv - tabela Filmy Gatunki z wagami
    Given Mając pliki movies, links i data
    When Kiedy zapisuje wazona tabele do pliku csv - helpers.weighted_genres_to_csv(movies_file, links_file, data_file)
    Then Pojawia się plik films_genres.csv

  Scenario: Generuje dataframe z wagami w zaleznosci od ilosci stwierdzonych gatunkow
    Given Majac pliki movies.csv, links.csv, i data.csv
    When kiedy wywoluje funkcje helpers.genres.weighted_film_genres(movies_file, links_file, data_file)
    Then Otrzymuje dataframe z wagami

  Scenario: Generuje plik imdb_movies.csv w oparciu o stwierdzone id filmow z bazy
    Given Mam listę identyfikatorow IMDB wystepujacych w bazie
    When Kiedy pobieram dane ze strony IMDB w oparciu o IMDB ID - helpers.genres.create_imdb_movies_csv(ids_file)
    Then Otrzymuje plik imdb_movies.csv
