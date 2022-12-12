import numpy as np
import random
from copy import deepcopy


class Product:
    def __init__(self, profit, amount_of_mt):
        """
        Uwzględniamy stałą liczbę maszyn, jednak zmienną ilość produktów. 
        :param profit: pozwala na zdefiniowanie przychodu za daną część
        :param amount_of_mt: ilość rodzajów maszyn, bezpośrednio związana z klasą Machines
        """
        self.profit = profit
        self.amount_of_mt = amount_of_mt

    def hps(self, *args):
        """
        funkcja zwracająca listę godzin potrzebnych na poszczególne maszyny
        :return: zwracana jest lista, która zawiera czas potrzebny do produkcji produktu na poszczególnych etapie
        """
        time_vector = list(args)
        if len(time_vector) == self.amount_of_mt:
            return np.transpose(time_vector)
        else:
            return 0

    def hps_matrix(self, *args):
        """
        funkcja łączy podane w parametrach wektory w macierz, w tym przypadku łączymy wektory transponowane z funkcji hps
        :return: zwraca macierz wektorów, które określają czas potrzebny na poszczególny etap
        """
        return np.column_stack(args)

    def profit_all_products(self, *args):
        """
        funkcja zwraca krotkę, zawierającą przychód osiągalny z poszczególnych części
        :return: zwraca krotkę, zawierającą przychód z poszczególnych części
        """
        return args


class Machines:
    def __init__(self, types):
        """
        Zakładamy, że istnieją zmienna ilość rodzajów maszyn
        :param types: mówi nam ile rodzajów maszyn uwzględniamy
        """
        self.types = types

    def amount_of_specific_type(self, *args):
        """
        funkcja pozwalająca na wprowadzenie ilości urządzeń danego rodzaju dostępnych w fabrycę
        :return: zwraca krotkę, liczb maszyn dostępnych na podanych kolejno etapach, zwraca 0 w przypadku gdy nie podano, wartości któregoś z parametrów lub podano ich za dużo
        """
        amount_tuple = args
        if len(amount_tuple) == self.types:
            return amount_tuple
        else:
            return 0


class Factory:
    default_hps = np.array([[0, 15, 25, 0],
                           [12, 6, 0, 14],
                           [10, 8, 0, 0]])

    default_profit = (600, 700, 500, 300)

    default_mps = (3, 3, 2)

    default_lpm = (150, 140, 90)

    def __init__(self, worker_hours=400, hours_per_stage=default_hps, profit=default_profit,
                 machines_per_stage=default_mps, limits_per_machine=default_lpm, checking_time=10):
        """
        :param worker_hours: zamiast przeliczać pracowników podajemy wprost ile godzin wypracują w sumie
        :param hours_per_stage: macierz zawierająca ile godzin trzeba poświęcić na danym etapie dla danej części
        :param profit: wektor niosący informacje ile zarabia się na i-tej części
        :param machines_per_stage: ilość maszyn dostępnych dla danego etapu
        :param limits_per_machine: ilość godzin maksymalnie na etap
        :param checking_time: czas potrzebny na sprawdzenie części po wykonaniu
        """
        self.workers_hours = worker_hours
        self.hours_per_stage = hours_per_stage
        self.profit = profit
        self.machines_per_stage = machines_per_stage
        self.limits_per_machine = limits_per_machine
        self.checking_time = checking_time



class Solution(Factory):
    def __init__(self):
        """
        :param workers_hours_left: pozostałe roboczogodziny
        :param hours_per_machine_left: pozostałe godziny na daną maszynę
        :param production_error: ograniczenie związane z faktem, ze przy małej ilości godzin nie jesteśmy w stanie zainicjować produkcji nowej części
        :param best_production: najlepsze dotychczasowe rozwiązanie tej samej postaci co parametr self.production
        :param best_funkcja_celu: funkcja celu z najlepszego rozwiązania
        W tej klasie zmieniamy ilość dostępnych zasobów
        """
        super().__init__(worker_hours=400, hours_per_stage=Factory.default_hps, profit=Factory.default_profit,
                 machines_per_stage=Factory.default_mps, limits_per_machine=Factory.default_lpm, checking_time=10)
        self.workers_hours_left = self.workers_hours
        self.hours_per_machine_left = list(self.limits_per_machine)
        self.production = [0 for _ in range(len(self.profit))]
        self.best_production = [0 for _ in range(len(self.profit))]
        self.best_funkcja_celu = 0
        self.production_error = 0
        self.tabu_list = []
        self.max_tabu_len = 10 # trzeba to przekazywac jako parametr

    def funkcja_celu(self):
        """
        funkcja obliczająca wartość funkcji celu
        :return: wartość funkcji celu
        """
        suma = 0
        for i in range(len(self.production)):
            suma += self.production[i] * self.profit[i]
        return suma

    def ograniczenia(self):
        """
        funkcja sprawdzająca czy zachowane są odgórnie narzucone ograniczenia
        :return: zwraca błąd gdy niezachowane jest dane ograniczenie, 1 oznacza rozwiązanie niedopuszczalne, 0 rozwiązanie dopuszczonalne
        """
        requirements = np.zeros(len(self.profit))
        req_worker = 0

        for i in range(self.hours_per_stage.shape[0]):
            for j in range(self.hours_per_stage.shape[1]):
                requirements[i] += self.hours_per_stage[i][j] * self.production[j]
                if requirements[i] > 5 * 8 * self.machines_per_stage[i]: # 5 (dni tygodnia) * 8 (roboczogodzin dziennie) * ilość maszyn na danym etapie
                    return 1
            req_worker += self.checking_time * self.production[i] + requirements[i]
            if req_worker > self.workers_hours:
                return 1
        return 0

    def random_solution(self):
        if self.best_funkcja_celu == 0:                              # wyznaczanie startowego losowego rozwiązania
            while self.workers_hours_left > 0 and self.production_error <= 10:
                self.random_part()
            self.production_error = 0
            if self.best_funkcja_celu == 0:
                self.best_production = deepcopy(self.production)
                self.best_funkcja_celu = self.funkcja_celu()
        else:                                                        # wyznaczanie losowego rozwiązanie, ale nie startowego
            self.workers_hours_left = self.workers_hours  
            self.hours_per_machine_left = list(self.limits_per_machine)
            self.production = [0 for _ in range(len(self.profit))]
            while self.workers_hours_left > 0 and self.production_error <= 10:
                self.random_part()
            self.production_error = 0
            if self.funkcja_celu() > self.best_funkcja_celu and not self.ograniczenia():
                self.best_production = deepcopy(self.production)
                self.best_funkcja_celu = self.funkcja_celu()              

    def random_part(self, banned_part=np.inf):
        while 1:
            part_number = random.randint(0, self.hours_per_stage.shape[1]-1)
            if part_number != banned_part:
                break
        if np.sum(self.hours_per_stage[:, part_number]) + self.checking_time > self.workers_hours_left:
            self.production_error += 1
            return
        for i in range(self.hours_per_stage.shape[0]):
            if self.hours_per_stage[i, part_number] > self.hours_per_machine_left[i]:
                self.production_error += 1
                return
        for i in range(self.hours_per_stage.shape[0]):
            self.hours_per_machine_left[i] -= self.hours_per_stage[i, part_number]
            self.workers_hours_left -= self.hours_per_stage[i, part_number]
        self.workers_hours_left -= self.checking_time
        self.production[part_number] += 1  # dodaje przedmiot do wektora rozwiązań
        #tu można zmienić żeby ograniczenia sprawdzałą funkcja a jeśli nie są spełnione to reverse_changes()

    def change_neighbour(self, neigh_type='default'):
        """
        funkcja do zmiany sąsiada - zależnie od tego, jaki jest 'typ sąsiedztwa', tak zostanie zmienione rozwiązanie
        :param neigh_type: typ sąsiedztwa, domyślnie default - jeden produkt usunięty z rozwiązania i wypełnienie
                            pozostałych roboczogodzin innymi produktami
        """
        if neigh_type == 'default':
            initial_production = deepcopy(self.production)
            part_number = random.randint(0, self.hours_per_stage.shape[1]-1) # losuję produkt do usunięcia
            if self.production[part_number] > 0: # sprawdzam czy w ogóle taka część ma być produkowana
                self.production[part_number] -= 1
                self.workers_hours_left += self.checking_time
                for i in range(self.hours_per_stage.shape[0]):
                    self.hours_per_machine_left[i] += self.hours_per_stage[i, part_number]
                    self.workers_hours_left += self.hours_per_stage[i, part_number]
                while self.workers_hours_left > 0 and self.production_error < 10: # tu można zamiast stałej dać parametr
                    self.random_part(part_number)  # zabraniam dodawania odjętego produktu - tylko otoczenie a nie sąsiedztwo
                if self.production in self.tabu_list:  # jeśli to jest zabronione przejście, to odwróć zmiany
                    self.reverse_changes(initial_production)
                    # print('zabronione')
                else:
                    self.tabu_list.append(deepcopy(self.production))  # dodaję rozwiązanie do listy tabu
                    if self.funkcja_celu() > self.best_funkcja_celu and not self.ograniczenia():  # zapamiętywanie najlepszego rozwiązania
                        self.best_production = deepcopy(self.production)
                        self.best_funkcja_celu = self.funkcja_celu()
                    if len(self.tabu_list) > self.max_tabu_len:  # sprawdzam czy lista tabu nie jest za długa
                        self.tabu_list.pop(0)
                self.production_error = 0 # wyzerowanie tego errora żeby przy kolejnych iteracjach szło od zera
            else:
                self.change_neighbour()

    def reverse_changes(self, previous_state):
        """
        zmienia production do wcześniejszego stanu
        :param previous_state: stan do którego ma wrócić production
        """
        for i in range(len(self.production)):
            while self.production[i] != previous_state[i]:
                if self.production[i] > previous_state[i]:
                    self.production[i] -= 1
                    self.workers_hours_left += self.checking_time
                    for j in range(self.hours_per_stage.shape[0]):
                        self.hours_per_machine_left[j] += self.hours_per_stage[j, i]
                        self.workers_hours_left += self.hours_per_stage[j, i]
                elif self.production[i] < previous_state[i]:
                    self.production[i] += 1
                    self.workers_hours_left -= self.checking_time
                    for j in range(self.hours_per_stage.shape[0]):
                        self.hours_per_machine_left[j] -= self.hours_per_stage[j, i]
                        self.workers_hours_left -= self.hours_per_stage[j, i]

    # TODO: trzeba dodać taką główną funkcję do wyszukiwania nowych sąsiadów w pętli już i ewentualnie jakiś inny sposób
    # TODO: na wyszukiwanie nowego sąsiada


class TabuSearch():
    def __init__(self, solution, max_iter=100, stopping_cond=None, neigh_type='default', aspiration_criteria='default'):
        """
        :param solution: startowe rozwiązanie, obiekt klasy Solution
        :param max_tabu_len: wielkość listy tabu
        :param max_iter: maksymalna liczba iteracji
        :param stopping_cond: warunek przerywający działanie algorytmu, inny niż liczba iteracji
        :param neighbourhood: rodzaj stosowanego sąsiedztwa
        :param aspiration_criteria: rodzaj stosowanego kryterium aspiracji
        """
        self.solution = solution
        self.max_tabu_len = solution.max_tabu_len
        self.stopping_cond = stopping_cond
        self.max_iter = max_iter
        self.neigh_type = neigh_type
        self.aspiration_criteria = aspiration_criteria

    def next_move(self):
        """
        funkcja wykonująca krok
        """
        self.solution.change_neighbour()

    def algorythm(self, aspiration_counter=20):
        """
        funkcja zawierająca główną pętlę algorytmu, kryterium aspiracji wykona ruch do losowego rozwiązania po określonej liczbie 
        iteracji od ostatniej aktualizacji najlepszego rozwiązania
        :param aspiration_counter: po ilu iteracjach zastosować kryterium aspiracji
        :return: krotka zawierająca optymalny rozkład produkcji i wartość funkcji celu
        """
        iter = 0  # liczba iteracji
        counter = 0  # liczba iteracji od poprzedniej aktualizacji najlepszego rozwiązania
        best = sol.best_funkcja_celu  # najlepsze rozwiązania (wartość funkcji celu)
        while iter < self.max_iter and not self.stopping_cond:
            self.next_move()
            iter += 1
            print(sol.production, sol.funkcja_celu(), sol.ograniczenia())
            
            # kryterium aspiracji
            if best == sol.best_funkcja_celu:
                counter += 1
                if counter == aspiration_counter:
                    sol.random_solution()
                    counter = 0
            else:
                best = sol.best_funkcja_celu
                counter = 0
            print(counter)
        return self.solution.best_production, self.solution.best_funkcja_celu
        


#Zdefiniowanie ilości maszyn
mach = Machines(3)
machines_per_stage = mach.amount_of_specific_type(3, 3, 2)

#Zdefiniowanie produktów
prod1 = Product(600, mach.types)
vec1 = prod1.hps(0, 12, 10)
prod2 = Product(700, mach.types)
vec2 = prod2.hps(15, 6, 8)
prod3 = Product(500, mach.types)
vec3 = prod3.hps(25, 0, 0)
prod4 = Product(300, mach.types)
vec4 = prod4.hps(0, 14, 0)

#Przygotowanie potrzebnych macierzy i wektorów
hps_matrix = prod1.hps_matrix(vec1, vec2, vec3, vec4)
profits = prod1.profit_all_products(prod1.profit, prod2.profit, prod3.profit, prod4.profit)

# print(profits)
# print(hps_matrix)

sol = Solution()
sol.random_solution()
# print('Funkcja celu:', sol.funkcja_celu())
# print('Jak 0 to ok: ', sol.ograniczenia())
# print('Ile jakich części: ', sol.production)
# # print(sol.best_production)
# sol.change_neighbour()
# print('Sąsiad:', sol.production)
# print('Funkcja celu:', sol.funkcja_celu())
# sol.reverse_changes(sol.best_production)
# print('Poprzednia produkcja: ', sol.production)

ts = TabuSearch(sol)
print(ts.algorythm(10))