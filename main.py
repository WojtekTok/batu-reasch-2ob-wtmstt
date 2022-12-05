import numpy as np
import random


class Factory:
    default_hps = np.array([0, 15, 25, 0],
                           [12, 6, 0, 14],
                           [10, 8, 0, 0])

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
        self.production = self.random_solution()  # tu będzie wywoływana funckja do wyliczenia pierwszego rozwiązania - lista z intami

    def funkcja_celu(self):
        """
        funkcja obliczająca wartość funkcji celu
        :return: wartość funkcji celu
        """
        suma = 0
        for i in range(len(self.production)):
            suma += self.production[i] * self.profit[i]
        return suma

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

    def random_solution(self):
        while self.workers_hours > 0: # TODO:dodać że jeśli nie znajdzie nic więcej niż ileśtam razy to też przerywa petle
            self.random_part()

    def random_part(self):
        part_number = random.randint(0, self.hours_per_stage.shape[1])
        for i in range(self.hours_per_stage[0]):
            if self.hours_per_stage[i][part_number] > self.hours_per_machine_left[i] or self.hours_per_stage[i][part_number] > self.workers_hours_left:
                self.hours_per_machine_left[i] -= self.hours_per_stage[i][part_number]
                self.workers_hours_left -= self.hours_per_stage[i][part_number]
        self.production[part_number] += 1  # dodaje przedmiot do wektora rozwiązań
