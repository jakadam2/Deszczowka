# Plan oraz estymacja projektu

**Cel** - stworzenie narzędzia pozwalającego na zbudowanie modelu, który na podstawie prognozy będzie w stanie estymować wartość odczytu z konkretnego deszczomierzu (model per deszczomierz)

**Model** - na wejściu powinien mieć prognozę (lub ich zbiór) dla konkretnego obszaru i na wyjściu zwracać konkretną liczbę (lub ich serie) - stan/y deszczomierza

**Plan:**
1. **Pozyskanie danych**
   1. Dane z prognozy pogody
      1. Modele ALARO, AROME co 6h  
      2. **Opcjonalnie** - Modele MERGE, co 10min
      3. Sparsowanie i standaryzacja 
   2. Dane z deszczomierzy
      1. Dane z IMGW co 10min
      2. Sparsowanie i standaryzacja
2. **Konstrukcja oraz trening modeli**
   - Wybór modelu
      1. Regresja liniowa - baseline
      2. Drzewa decyzyjne takie jak `XGBoost`, `CatBoost`, `LightGBM`
      3. Sieci neuronowe
         1. `MLPRegressor`
         2. `Conv2D`
         3. `LSTM`
         4. **Opcjonalnie** - Bardziej zaawansowane architektury
      4. **Opcjonalnie** - Zaawansowane modele takie jak `Moment`, `ARIMA`, `ETS`
   - Trening modelu
      1. Podział na zbiór treningowy i testowy zgodnie z metodykami stosowanymi w uczeniu maszynowym na szeregach czasowych
      2. Optymalizacja hiperparametrów dla każdego z modeli
      3. Ewaluacja wyników
         1. Wybór metryki ewaluacji
         2. Porównanie wyników dla różnych modeli
         3. **Opcjonalnie** - Porównanie wyników dla różnych deszczomierzy
      4. **Opcjonalnie** - Transfer learning pomiędzy deszczomierzami
3. **Stworzenie pipelinu/frameworku/biblioteki pozwalającego na ewaluację modeli dla standaryzacji badań**
   1. Stworzenie pipelinu
   2. Integracja z `MLFlow` lub `WandB`
   3. **Opcjonalnie** - Stworzenie frameworku