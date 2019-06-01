Feature: Tworzymy UserProfile - czyli profil uzytkownika

 user profile - czyli
 wziac id filmow ocenionych przez uzykownika (rozne od Nan)
 pobrac z dataframe film/genres dany film
 i dodac do odpowiedniego gatunku wartosci wag do profilu uzytkownika
 i jednoczesnie dodac (jak 1/3 lub 1/2??) ilosc obejrzanych przez uzytkownika filmow z danego gatunku

 profil powinien wygladać nastepująco
 { user_id :
       { 'Action' : 34.4345,
         'number_of_watched' : 23 },
       { 'Drama' : 17.315,
         'number_of_watched' : 13 },
 } itd.

 dalej liczymy średnią czyli
           Action      Drama       Comedy      Horror      Sci-Fi
   value     15          8            4           3           1          średnia   31 /  5  = 6,20 (ilość gatunków)
   number     3          2            3           7           7
   avg       6.2        6.2          6.2         6.2         6.2
   delta    8.80       1.80        -2.20       -3.20       -5.20        delta = value - avg

 sortujemy malejąco po delta
          [ 8.80,      1.80,       -2.20 ,     -3.20,      -5.20 ]

 chcemy uzyskać uzytkownika który preferuje pewne gatunki
 wiec delta #1 pozycji > jak 2 x średnia (avg)
 wiec delta #2 pozycji > 50 % delty #1
 wiec delta #3 pozycji > 30 # delty #1

  Scenario: # Enter scenario name here
    # Enter steps here