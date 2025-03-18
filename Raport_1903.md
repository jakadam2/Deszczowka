# Analiza problemu i dziedziny

## Linki do artykułów
- [AROME](https://www.umr-cnrm.fr/IMG/pdf/arome2007.en.pdf) 
- [Overview](https://iwaponline.com/hr/article/4/3/171/1358/NUMERICAL-SIMULATION-OF-THE-RAINFALL-RUNOFF)

---
## Zbiory danych
Sensownym dla naszych potrzeb wydaje się być zbiór danych IMGW-PIB. Udostępniają tam dane historyczne z dokładnością również z prognozami innych modeli.
- [IMGW-PIB](https://danepubliczne.imgw.pl/pl/datastore)

Dodatkowo mamy XRain, który oferuje dane z całego świata, natomiast dostęp do nich jest blokowany i wymagane jest założenie konta. Co więcej, strona jest w posiadaniu przez Japończyków, więc połączenie jest stosunkowo wolne.
- [XRain](https://diasjp.net/en/)

---
## Modelowanie opadów
### Numeryczne - mamy model któremu ustawiamy parametry i on na ich podstawie prowadzi symulacji 
- AROME - numeryczny i do małej skali, wydaje się być ok dla nas

### Stochastyczne - opieramy się na dostarczonych danych
- [tu](https://www.sciencedirect.com/science/article/pii/S0022169417304390) jest chyba fajny przykład 
- [tu tez](https://www.sciencedirect.com/science/article/pii/S0022169416302542)

### ML - łączy się to z kategorią wyżej
- Mozna symulować za pomoca [nieparametrycznego MLa](https://www.sciencedirect.com/science/article/pii/S0378475499000166), KNN, ale to chyba moze nie byc najlepsze rozwiazanie dla naszego problemu 
- Podejście z modelowaniem [szeregów czasowych](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1002/2017WR020876)

### DL
- Można spróbować połączyć modele służące do szeregów czasowych razem z warstwami konwolucyjnymi, natomiast może to wymagać bardzo dużej ilości zasobów obliczeniowych.

---
## Metody używane do rozwiązania problemu
