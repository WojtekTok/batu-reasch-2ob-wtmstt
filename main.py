import numpy as np
import random
import tkinter as tk
from copy import deepcopy


class Product:
    def __init__(self, profit, amount_of_mt):
        """
        Uwzględniamy zmienną liczbę maszyn oraz zmienną ilość produktów. 
        :param profit: pozwala na zdefiniowanie przychodu za daną część
        :param amount_of_mt: ilość rodzajów maszyn, bezpośrednio związana z klasą Machines
        """
        self.profit = profit
        self.amount_of_mt = amount_of_mt

    def hps(self, *args):
        """
        funkcja zwracająca listę godzin potrzebnych na poszczególne maszyny
        :param *args: jako argument podawana jest krotka przedstawiająca, ilość czasu potrzebnego na produkcję danego rodzaju produktu 
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
        :param *args: podawane są wektory, które wykorzystane są następnie do połączenia i utworzenia macierzy
        :return: zwraca macierz wektorów, które określają czas potrzebny na poszczególny etap
        """
        return np.column_stack(args)

    def profit_all_products(self, *args):
        """
        funkcja zwraca krotkę, zawierającą przychód osiągalny z poszczególnych części
        :param *args: wprowadzana jest krotka, przedstawiająca przychód z poszczególnych produktów
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
        :param *args:
        :return: zwraca krotkę, liczb maszyn dostępnych na podanych kolejno etapach, zwraca 0 w przypadku gdy nie podano, wartości któregoś z parametrów lub podano ich za dużo
        """
        amount_tuple = args[0]
        print(amount_tuple)
        if len(amount_tuple) == self.types:
            return amount_tuple
        else:
            return 0

class Workers:
    def __init__(self, amount_of_workers, checking_time, days_of_work = 5, hours_per_day = 8):
        """
        Zakładamy zmienną liczbę pracowników oraz zmienny tydzień pracy, możliwa modyfikacja również parametru odpowiedzialnego za sprawdzanie jakości
        :param amount_of_workers: ilość dostępnych pracowników
        :param checking_time: czas potrzebny na sprawdzenie jakości
        :param days_of_work: dni pracy
        :param hours_per_day: godziny dziennie poświecone na pracę przez pracownika
        """
        self.amount_of_workers = amount_of_workers
        self.days_of_work = days_of_work
        self.hours_per_day = hours_per_day
        self.checking_time = checking_time
    
    def worker_hours(self):
        """
        funkcja zwraca ilość godzin możliwych do przeznaczenia na produkcję w fabryce
        :return: zwracana jest ilość dostępnych godzin zasobów ludzkich
        """
        return self.amount_of_workers * self.days_of_work * self.hours_per_day
        

class Factory:
    default_hps = np.array([[0, 15, 25, 0],
                           [12, 6, 0, 14],
                           [10, 8, 0, 0]])

    default_profit = (600, 700, 500, 300)

    default_mps = (3, 3, 2)

    default_lpm = (150, 140, 90)

    def __init__(self, hours_per_stage=default_hps, profit=default_profit,
                 machines_per_stage=default_mps, limits_per_machine=default_lpm, checking_time=10, worker_hours=400):
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
    def __init__(self, max_tabu_len, tabu_type, hours_per_stage=Factory.default_hps, profit=Factory.default_profit,
                 machines_per_stage=Factory.default_mps, limits_per_machine=Factory.default_lpm, checking_time=10, worker_hours=400, days_of_work = 5, hours_per_day = 8):
        """
        :param previous_funkcja_celu: parametr wykorzystywany do algorytmu z deterministyczną listą tabu, aby porównywać kolejne kroki
        :param max_tabu_len: startowa długość listy tabu (dla tabu_type = const)
        :param current_tabu_len: obecna długość listy tabu (dla tabu_type = deterministic)
        :param tabu_type: constant/deterministic lista tabu pozostaje stałej długości lub jest deterministyczna
        :param workers_hours_left: pozostałe roboczogodziny
        :param hours_per_machine_left: pozostałe godziny na daną maszynę
        :param production_error: ograniczenie związane z faktem, ze przy małej ilości godzin nie jesteśmy w stanie zainicjować produkcji nowej części
        :param best_production: najlepsze dotychczasowe rozwiązanie tej samej postaci co parametr self.production
        :param best_funkcja_celu: funkcja celu z najlepszego rozwiązania
        :param best5_productions: tablica zawierająca (5) krotek z najlepszymi liniami produkcyjnymi, ich funkcją cel, roboczogodzinami oraz godzina na daną maszynę
        W tej klasie zmieniamy ilość dostępnych zasobów
        """
        super().__init__(worker_hours=worker_hours, hours_per_stage=hours_per_stage, profit=profit,
                 machines_per_stage=machines_per_stage, limits_per_machine=limits_per_machine, checking_time=checking_time)
        self.workers_hours_left = self.workers_hours
        self.hours_per_machine_left = [days_of_work * hours_per_day * self.machines_per_stage[i] for i in range(len(self.machines_per_stage))]#list(self.limits_per_machine)
        self.production = [0 for _ in range(len(self.profit))]
        self.best_production = [0 for _ in range(len(self.profit))]
        self.best_funkcja_celu = 0
        self.previous_funkcja_celu = 0
        self.production_error = 0
        self.tabu_list = []
        self.best5_productions = [(0, 0) for _ in range(5)]
        self.max_tabu_len = max_tabu_len
        self.current_tabu_len = max_tabu_len
        self.tabu_type = tabu_type
        self.part_probability = self.calculate_probability()
        self.reversed_probability = self.calculate_reversed_probability()
        self.day_of_work = days_of_work
        self.hours_per_day = hours_per_day

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
                if requirements[i] > self.hours_per_day * self.day_of_work * self.machines_per_stage[i]: # 5 (dni tygodnia) * 8 (roboczogodzin dziennie) * ilość maszyn na danym etapie
                    # print('Zostało godzin na maszyne', self.hours_per_machine_left)
                    return 1
            req_worker += self.checking_time * self.production[i] + requirements[i]
            if req_worker > self.workers_hours:
                print('Zostało godzin: ', self.workers_hours_left)
                return 1
        return 0

    def random_solution(self):
        """
        znajdowanie pierwszego, losowego rozwiązania
        :return:
        """
        if self.best_funkcja_celu == 0:                              # wyznaczanie startowego losowego rozwiązania
            while self.workers_hours_left > 0 and self.production_error <= 10:
                self.random_part()
            self.production_error = 0
            if self.best_funkcja_celu == 0:
                self.best_production = deepcopy(self.production)
                self.best_funkcja_celu = self.funkcja_celu()
            if self.tabu_type == 'deterministic':
                self.previous_funkcja_celu = self.funkcja_celu()
        else:                                                        # wyznaczanie losowego rozwiązanie, ale nie startowego
            if self.tabu_type == 'deterministic':
                self.current_tabu_len = self.max_tabu_len                       # resetuje parametry rozwiązania do startowych 
            self.workers_hours_left = self.workers_hours  
            self.hours_per_machine_left = [self.day_of_work * self.hours_per_day * self.machines_per_stage[i] for i in range(len(self.machines_per_stage))]
            self.production = [0 for _ in range(len(self.profit))]
            while self.workers_hours_left > 0 and self.production_error <= 10:
                self.random_part()
            self.production_error = 0
            if self.funkcja_celu() > self.best_funkcja_celu and not self.ograniczenia():
                self.best_production = deepcopy(self.production)
                self.best_funkcja_celu = self.funkcja_celu()
            if self.tabu_type == 'deterministic':
                self.previous_funkcja_celu = self.funkcja_celu()
                self.current_tabu_len = self.max_tabu_len

    def random_best_solution(self):
        """
        wybieram losowe spośród kilku najlepszych rozwiązań i zastępuje nim obecne rozwiązanie
        """          
        while 1:
            random_no = random.randint(0, len(self.best5_productions) - 1)
            if self.best5_productions[random_no][0] != 0:
                break
        random_sol = self.best5_productions[random_no]
        self.best5_productions[random_no] = (0, 0, 0, 0)

        self.production = deepcopy(random_sol[1])
        self.workers_hours_left = deepcopy(random_sol[2])
        self.hours_per_machine_left = deepcopy(random_sol[3])
        self.best5_productions = sorted(self.best5_productions, reverse=True)
        if self.tabu_type == 'deterministic':
            self.previous_funkcja_celu = self.funkcja_celu()
            self.current_tabu_len = self.max_tabu_len

    def random_part(self, banned_part=np.inf, type='default'):
        """
        funkcja dodająca losową część do rozwiązania
        :param banned_part: część której nie można wybrać
        :param type: typ wybierania części - losowy lub deterministyczny
        :return:
        """
        while 1:
            if type == 'default':
                part_number = random.randint(0, self.hours_per_stage.shape[1]-1)
            elif type == 'deterministic':
                part_number = np.random.choice(np.arange(0, len(self.profit)), p=self.part_probability)
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

    def change_neighbour(self, neigh_type='default', del_selection='default'):
        """
        funkcja do zmiany sąsiada - zależnie od tego, jaki jest 'typ sąsiedztwa', tak zostanie zmienione rozwiązanie
        :param neigh_type: typ sąsiedztwa, domyślnie default - jeden produkt usunięty z rozwiązania i wypełnienie
                            pozostałych roboczogodzin innymi produktami
        :param del_selection: sposób wybierania części do usunięcia z produkcji
        """
        initial_production = deepcopy(self.production)
        if del_selection == 'default':
            part_number = random.randint(0, self.hours_per_stage.shape[1]-1) # losuję produkt do usunięcia
        elif del_selection == 'deterministic':
            part_number = np.random.choice(np.arange(0, len(self.profit)), p=self.reversed_probability)
        if self.production[part_number] > 0: # sprawdzam czy w ogóle taka część ma być produkowana
            self.production[part_number] -= 1
            self.workers_hours_left += self.checking_time
            for i in range(self.hours_per_stage.shape[0]):
                self.hours_per_machine_left[i] += self.hours_per_stage[i, part_number]
                self.workers_hours_left += self.hours_per_stage[i, part_number]
            while self.workers_hours_left > 0 and self.production_error < 10: # tu można zamiast stałej dać parametr
                self.random_part(part_number, type=neigh_type) # zabraniam dodawania odjętego produktu - tylko otoczenie a nie sąsiedztwo
            if self.production in self.tabu_list:  # jeśli to jest zabronione przejście, to odwróć zmiany
                self.reverse_changes(initial_production)
            else:
                self.tabu_list.append(deepcopy(self.production))  # dodaję rozwiązanie do listy tabu
                if self.funkcja_celu() > self.best_funkcja_celu and not self.ograniczenia():  # zapamiętywanie najlepszego rozwiązania
                    self.best_production = deepcopy(self.production)
                    self.best_funkcja_celu = self.funkcja_celu()
                
                if self.tabu_type == 'constant':
                    if len(self.tabu_list) > self.max_tabu_len:  # sprawdzam czy lista tabu nie jest za długa
                        self.tabu_list.pop(0)
                elif self.tabu_type == 'deterministic':
                    if len(self.tabu_list) > self.current_tabu_len:  # sprawdzam czy lista tabu nie jest za długa
                        self.tabu_list.pop(0)
                
                if self.tabu_type == 'deterministic':
                    if self.funkcja_celu() + 100 < self.previous_funkcja_celu:  # zmniejszamy listę tabu przy jakimś warunku
                        self.current_tabu_len -= 1
                    elif self.funkcja_celu() > self.previous_funkcja_celu + 100:  # powiększamy listę przy jakimś warunku
                        self.current_tabu_len += 1

                if self.funkcja_celu() > self.best5_productions[-1][0] and not self.ograniczenia():    # zapamiętywanie kilku najlepszych rozwiązań, potem użwamy do kryterium aspiracji
                    already_on_list = False
                    for i in range(len(self.best5_productions)):
                        if self.production == self.best5_productions[i][1]:
                            already_on_list = True
                            break
                    if not already_on_list:
                        self.best5_productions[-1] = (self.funkcja_celu(), deepcopy(self.production), deepcopy(self.workers_hours_left), deepcopy(self.hours_per_machine_left))
                        self.best5_productions = sorted(self.best5_productions, reverse=True)
                    else:
                        already_on_list = False
                if self.tabu_type == 'deterministic':
                    self.previous_funkcja_celu = self.funkcja_celu()
            self.production_error = 0 # wyzerowanie tego errora żeby przy kolejnych iteracjach szło od zera
        else:
            self.change_neighbour(neigh_type=neigh_type)

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

    def calculate_probability(self):
        probab = [0 for _ in range(len(self.profit))]  # suma godzin dla danej czesci
        suma = 0
        for i in range(len(self.profit)):
            for machines in range(len(self.machines_per_stage)):
                probab[i] += self.hours_per_stage[machines, i]
            probab[i] = self.profit[i] / probab[i]
            suma += probab[i]
        for i in range(len(probab)):
            probab[i] /= suma
        return probab

    def calculate_reversed_probability(self):
        """
        funkcja obliczająca w miarę odwrotne prawdopodoieństwo - idealnie byc nie musi :D
        :return: odwrotne prawdopodobieństwo
        """
        avg_prob = 1/len(self.profit)
        rev_prob = [0 for _ in range(len(self.profit))]
        for i in range(len(self.part_probability)):
            rev_prob[i] = avg_prob - (self.part_probability[i]-avg_prob)
        return rev_prob


class TabuSearch():
    def __init__(self, solution, neigh_type='default', del_selection='default', aspiration_criteria='random', max_iter=100, aspiration_threshold=10):
        """
        :param solution: startowe rozwiązanie, obiekt klasy Solution
        :param max_iter: maksymalna liczba iteracji
        :param aspiration_threshold: po ilu iteracjach może nastąpić reset rozwiązania
        :param stopping_cond: warunek przerywający działanie algorytmu, inny niż liczba iteracji
        :param neighbourhood: rodzaj stosowanego sąsiedztwa
        :param aspiration_criteria: rodzaj stosowanego kryterium aspiracji
        :param all_solutions: tablica zapisują wszystkie funkcje celu po kolei
        """
        self.solution = solution
        self.max_iter = max_iter
        self.neigh_type = neigh_type
        self.del_selection = del_selection
        self.aspiration_criteria = aspiration_criteria
        self.aspiration_threshold = aspiration_threshold
        self.all_solutions = []
        self.best_solutions = []
        self.aspiration_points = []

    def next_move(self):
        """
        funkcja wykonująca krok
        """
        self.solution.change_neighbour(neigh_type=self.neigh_type, del_selection=self.del_selection)

    def algorythm(self):
        """
        funkcja zawierająca główną pętlę algorytmu, kryterium aspiracji wykona ruch do losowego rozwiązania po określonej liczbie 
        iteracji od ostatniej aktualizacji najlepszego rozwiązania
        :return: krotka zawierająca optymalny rozkład produkcji i wartość funkcji celu
        """
        iter = 0  # liczba iteracji
        counter = 0  # liczba iteracji od poprzedniej aktualizacji najlepszego rozwiązania
        best = self.solution.best_funkcja_celu  # najlepsze rozwiązania (wartość funkcji celu)
        while iter < self.max_iter:
            self.next_move()
            iter += 1
            print(self.solution.production, self.solution.funkcja_celu())
            self.all_solutions.append(self.solution.funkcja_celu())
            self.best_solutions.append(self.solution.best_funkcja_celu)
            # kryterium aspiracji
            if self.aspiration_criteria == 'random' and iter < self.max_iter:
                if best == self.solution.best_funkcja_celu:
                    counter += 1
                    if counter == self.aspiration_threshold:
                        self.solution.random_solution()
                        self.all_solutions.append(self.solution.funkcja_celu())
                        self.best_solutions.append(self.solution.best_funkcja_celu)
                        self.aspiration_points.append((len(self.all_solutions)-1, self.solution.funkcja_celu()))
                        counter = 0
                        iter += 1
                else:
                    best = self.solution.best_funkcja_celu
                    counter = 0
            # kryterium aspiracji, które idzie do jednego z najlepszych rozwiązań
            elif self.aspiration_criteria == 'random_best' and iter < self.max_iter:
                if best == self.solution.best_funkcja_celu:
                    counter += 1
                    if counter == self.aspiration_threshold:
                        self.solution.random_best_solution()
                        self.all_solutions.append(self.solution.funkcja_celu())
                        self.best_solutions.append(self.solution.best_funkcja_celu)
                        self.aspiration_points.append((len(self.all_solutions)-1, self.solution.funkcja_celu()))
                        counter = 0
                        iter += 1
                else:
                    best = self.solution.best_funkcja_celu
                    counter = 0

        return self.solution.best_production, self.solution.best_funkcja_celu
        

#Zdefiniowanie pracowników
work = Workers(10, 10)
work_time = work.worker_hours()

#Zdefiniowanie ilości maszyn
mach = Machines(3)
mpt_list = [3,3,2]
mpt = mach.amount_of_specific_type(mpt_list)

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

print(hps_matrix)

profits = prod1.profit_all_products(prod1.profit, prod2.profit, prod3.profit, prod4.profit)


#Korzystamy już z wpisywanych wartości
# sol = Solution(max_tabu_len=10, tabu_type='constant', hours_per_stage=hps_matrix, profit=profits, machines_per_stage=mpt, checking_time=work.checking_time, worker_hours=work_time, days_of_work=work.days_of_work, hours_per_day=work.hours_per_day)
# sol.random_solution()
# print(type(sol))

# ts = TabuSearch(solution=sol, neigh_type='default', del_selection='default',aspiration_criteria='random', max_iter=100, aspiration_threshold=10)
# print(ts.algorythm())
