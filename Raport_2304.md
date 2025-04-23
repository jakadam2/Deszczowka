# Plan oraz estymacja projektu

**Cel** - stworzenie narzędzia pozwalającego na zbudowanie modelu, który na podstawie prognozy będzie w stanie estymować wartość odczytu z konkretnego deszczomierzu (model per deszczomierz)

**Model** - na wejściu powinien mieć prognozę (lub ich zbiór) dla konkretnego obszaru i na wyjściu zwracać konkretną liczbę (lub ich serie) - stan/y deszczomierza

**Plan:**
1. **Pozyskanie danych**
   1. Dane z prognozy pogody
      1. Modele ALARO, AROME co 6h  
      2. ```Opcjonalnie``` Modele MERGE, co 10min
      3. Sparsowanie i standaryzacja 
   2. Dane z deszczomierzy
      1. ```[TBA]```
2. **Konstrukcja oraz trening modeli**
   1. Regresja liniowa - baseline
   2. Model wykorzystujący konwolucję 
   3. ```Opcjonalnie``` Model wykorzystujące szeregi czasowe
3. **Ewaluacja wyników**
   1. Ewaluacja wyników na innym wycinku czasu (np. na danych od stycznie do marca trenujemy, od marca do lipca testujemy)
   2. Ewaluacja wyników na podstawie wybranego podziału (np. 30% według wybranego rozkładu będzie stanowić zbiór testowy)
   3. Ewaluacja na co n-tym pomiarze (konkretny przypadek punkty wyżej, co n-ty pomiar trafia deterministycznie do zbioru testowego)
   4. ```Opcjonalnie``` Zaproponowanie innego sposobu ewaluacji
4. **Stworzenie pipelinu/frameworku pozwalającego zbudować model dla innych danych**
   1. Stworzenie pipelinu
   2. ```Opcjonalnie``` Stworzenie frameworku