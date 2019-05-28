Feature: Tabela pomocnicza User Ratings

  Tworzy tabelę pomocniczą user x ratings z pliku ratings.csv.
  Plik ratings.csv zawiera łącznie 100837 pozycji, z którego można uzyskac macierz
  zawierająca 9742 filmy i 610 uzytkownikow.

  W tej części tworzymy pomocniczą tabelę w oparciu o identyfikatory filmów
  zawartych w pliku data.csv (w głównym katalogu).

  Tabela pomocnicza ma zawierać dokłądnie 2926 filmy (tyle filmów jest wczytanych do bazy)
  i 610 uzytkowników z ratingami powyższych filmów

  Scenario: Pobranie identyfikatorow IMDB z linku zawartego w pliku data.csv do listy
    Given Posiadajac plik data.csv
    When Gdy uruchamiam helpers.data_csv.retrive_imdbid(data_file)
    Then Powinienem w pierwszym wierszu otrzymac identyfikator IMDB tt0499549

  Scenario: Lista identyfikatorow na potrzeby pliku ratings.csv
    Given Majac plik links.csv z kolumnami movieId oraz imdbId
    And I Jednoczesnie kiedy posiadam liste identyfikatorow imdbid z pliku data.csv
    When Kiedy uruchamiam funkcję helpers.data_csv.merge_ids(links_file, idmb_id_list)
    Then Otrzymuje listę id filmow ktore juz sa w bazie

  Scenario: Tworze plik stripped_ratings.csv
    Given Mając listę identyfikatorow filmow wystepujacych w bazie
    And oraz plik ratings.csv
    When kiedy uruchamiam funkcję helpers.data_csv.create_stripped_ratings_csv(ids_present_in_db,rating_file)
    Then otrzymam plik stripped_rating.csv