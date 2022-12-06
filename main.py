import numpy as np
import random

class Product:
    def __init__(self, product_id, profit, time_1, time_2, time_3) -> None:
        """
        Uwzględniamy stałą liczbę maszyn, jednak zmienną ilość produktów. 
        :param product_id: pozwala na identyfikację produktu na podstawie ID
        :param profit: pozwala na zdefiniowanie przychodu za daną część
        :param time_1: czas wymagany na pierwszym rodzaju maszyny
        :param time_2: czas wymagany na drugim rodzaju maszyny
        :param time_3: czas wymagany na trzecim rodzaju maszyny
        """
        self.product_id = product_id
        self.profit = profit
        self.time_1 = time_1
        self.time_2 = time_2
        self.time_3 = time_3

    def hps(self):
        """
        funkcja zwracająca listę godzin potrzebnych na poszczególne maszyny
        :return: zwracana jest lista, która zawiera czas potrzebny do produkcji produktu na poszczególnych etapie
        """
        return [self.time_1, self.time_2, self.time_3]

class Machines:
    def __init__(self, amount_1, amount_2, amount_3, max_time_1, max_time_2, max_time_3) -> None:
        """
        Zakładamy, że istnieją maksymalnie 3 rodzaje maszyn.
        :param amount_1: ilość maszyn 1-go rodzaju
        :param amount_2: ilość maszyn 2-go rodzaju
        :param amount_3: ilość maszyn 3-go rodzaju
        :param max_time_1: maksymalny czas pracy maszyn 1-go rodzaju
        :param max_time_2: maksymalny czas pracy maszyn 1-go rodzaju
        :param max_time_3: maksymalny czas pracy maszyn 1-go rodzaju
        """
        self.amount_1 = amount_1
        self.amount_2 = amount_2
        self.amount_3 = amount_3
        self.max_time_1 = max_time_1
        self.max_time_2 = max_time_2
        self.max_time_3 = max_time_3

    def mps(self):
        """
        funkcja zwracająca ilość maszyn na danym etapie
        :return: krotka zwracająca ilość maszyn na poszczególnym etapie
        """
        return (self.amount_1, self.amount_2, self.amount_3)

    def lpm(self):
        """
        funkcja zwracająca maksymalny czas pracy na poszczególnych etapach
        :return: krotka zawierająca maksymalny czas pracy na poszczególnych etapach
        """
        return (self.max_time_1, self.max_time_2, self.max_time_3)

class Factory():
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
        # self.best_solution = Solution()

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
        :return: zwraca błąd gdy niezachowane jest dane ograniczenie
        """
        x, y = self.hours_per_stage.shape
        requirements = np.zeros(len(self.profit))
        req_worker = 0

        for i in range(x):
            for j in range(y):
                requirements[i] += self.hours_per_stage[i][j] * self.production[j]
                if requirements[i] > self.limits_per_machine:
                    raise SystemError('Maszyna będzie pracować zbyt długo!') # TODO: zamienić SystemError na jakiś inny error, który łatwo "przechwycić
        
        for i in range(x):
            req_worker += self.checking_time * self.production[i]
            if req_worker > self.workers_hours:
                raise SystemError('Nie ma tyle dostępnych godzin')

    # def random_solution(self):
    #     production = [10] # nie wiem czy to tutaj czy do solution to wrzucic, jaki kto ma plan tak niech robi
    #     return production


class Solution(Factory):
    def __init__(self):
        """
        workers_hours_left: pozostałe roboczogodziny
        hours_per_machine_left: pozostałe godziny na daną maszynę
        W tej klasie zmieniamy ilość dostępnych zasobów
        """
        super().__init__(worker_hours=400, hours_per_stage=Factory.default_hps, profit=Factory.default_profit,
                 machines_per_stage=Factory.default_mps, limits_per_machine=Factory.default_lpm, checking_time=10)
        self.workers_hours_left = self.workers_hours
        self.hours_per_machine_left = list(self.limits_per_machine)
        self.production = np.zeros(len(self.profit))

    def random_solution(self):
        while self.workers_hours_left > 0: # TODO:dodać że jeśli nie znajdzie nic więcej niż ileśtam razy to też przerywa petle
            self.random_part()

    def random_part(self):
        part_number = random.randint(0, self.hours_per_stage.shape[1]-1)
        if np.sum(self.hours_per_stage[:, part_number]) + self.checking_time > self.workers_hours_left:
            return
        for i in range(self.hours_per_stage.shape[0]):
            if self.hours_per_stage[i, part_number] > self.hours_per_machine_left[i]:
                return
        for i in range(self.hours_per_stage.shape[0]):
            self.hours_per_machine_left[i] -= self.hours_per_stage[i, part_number]
            self.workers_hours_left -= self.hours_per_stage[i, part_number]
        self.workers_hours_left -= self.checking_time
        self.production[part_number] += 1  # dodaje przedmiot do wektora rozwiązań


sol = Solution()
sol.random_solution()
print()