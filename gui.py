from main import *
from tkinter import messagebox, Tk
from tkinter.filedialog import askopenfilename
import tkinter as tk
from PIL import Image, ImageTk


class Gui():

    def __init__(self, worker=Workers(1,1), mach=Machines(1), prod=Product(1,1), workers_hours=0, amt_tuple=0, profits = [], hps_matrix = [], aspiration='random', tabu_search = 'default', del_selection='default', neigh_type='default', sol=[], max_iter=100, threshold=10):
        """
        Zdefiniowanie zmiennych tak, żeby mieć do nich dostęp w całej klasie
        :param worker: instancja klasy Workers
        :param mach: instancja klasy Machines
        :param prod: instancja klasy Product
        :param workers_hours: dostepny czas pracownikow
        :param amt_tuple: amount of types, krotka zawierająca ilość maszyn danego rodzaju
        :param profits: lista zawierająca zysk z poszczególnych produktów
        :param hps_matrix: macierz zawierająca czas potrzebny na wykonanie produktów na poszczególnym etapie
        :param aspiration: pozwala na wybranie rodzaju kryterium aspiracji
        :param ts: pozwala na definiowanie rodzaju potencjalnych zmian listy tabu
        :param del_selection: pozwala na wybranie rodzaju usuwania elementów
        :param neigh_type: pozwala na wybranie rodzaju sasiedztwa
        :param sol: intancja klasy Solution
        :param max_iter: maksymalna ilosc iteracji
        :param threshold: threshold
        """
        self.worker = worker
        self.mach = mach
        self.prod = prod
        self.wrk_hrs = workers_hours
        self.amt_tuple = amt_tuple
        self.profits = profits
        self.hps_matrix = hps_matrix
        self.aspiration = aspiration
        self.ts = tabu_search
        self.del_selection = del_selection
        self.neigh_type = neigh_type
        self.sol = sol
        self.max_iter = max_iter
        self.threshold = threshold


        #GUI
        self.root = tk.Tk()
        self.root.title('Fabryka - algorytm TS')
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap(r"ikona.ico")


        #Zmienne do checkbox'ow
        self.default_aspiration = tk.IntVar()
        self.one_of_best_aspiration = tk.IntVar()

        self.default_deletion = tk.IntVar()
        self.deterministic_deletion = tk.IntVar()

        self.default_neigh = tk.IntVar()
        self.deterministic_neigh = tk.IntVar()

        self.default_ts = tk.IntVar()
        self.deterministic_ts = tk.IntVar()


        #Wczytywanie danych z pliku i zapisywanie danych do pliku
        """
        :param button_load: wczytanie danych do pliku txt
        :param button_save: zapisywanie danych do pliku txt
        :param show_data: pozwala na zobaczenie aktualnych wartości zmiennych
        """

        #Buttons
        self.button_load = tk.Button(self.root, text='Load from file', relief=tk.RAISED, command = self.load_from_file).place(x=5, y=5)

        self.button_save = tk.Button(self.root, text='Save to file', relief=tk.RAISED, command=self.save_to_file).place(x=105, y=5)

        self.button_show_data = tk.Button(self.root, text='Show data', relief=tk.RAISED, command=self.new_window).place(x=605, y=5)


        #Pierwsza część modyfikowalna - utworzenie instancji klasy Workers
        """
        :param label_worker/entry_worker: label oraz wprowadzenie ilości pracowników
        :param label_ct/entry_ct: label oraz wprowadzenie wartosci checking_time (w godzinach)
        :param label_dow/entry_dow: label oraz wprowadzenie wartości dni pracy w tygodniu (nieobowiązkowe)
        :param label_hpd/entry_hpd: label oraz wprowadzenie wartości godzin pracy w ciągu dnia (nieobowiązkowe)
        :param set_workers_button: umożliwia utworzenie instancji klasy Workers z ustawionymi parametrami
        """

        #Labels
        self.label_worker = tk.Label(self.root, text='Enter the number of workers:').place(x=5, y=40)

        self.label_ct = tk.Label(self.root, text='Enter time required to check time:').place(x=205, y=40)

        self.label_dow = tk.Label(self.root, text='Enter days of work:').place(x=405, y=40) 

        self.label_hpd = tk.Label(self.root, text='Enter hours per day:').place(x=605, y=40)

        #Entries
        self.entry_worker = tk.Entry(self.root).place(x=5, y=60, width=50)

        self.entry_ct = tk.Entry(self.root).place(x=205, y=60, width=50)

        self.entry_dow = tk.Entry(self.root).place(x=405, y=60, width=50)

        self.entry_hpd = tk.Entry(self.root).place(x=605, y=60, width=50)

        #Buttons
        self.set_workers_button = tk.Button(self.root, text = 'Set Workers instance', relief=tk.RAISED, command=self.get_number_of_workers).place(x=5, y=85)


        #Druga część modyfikowalna - utworzenie instancji klasy Machines
        """
        :param label_types/entry_types: label oraz wprowadzenie ilości rodzajów maszyn na produkcji
        :param label_amt_tom/entry_amt_tom: label oraz wprowadzenie (amount_types_of_machines) ilość maszyn danego rodzaju w postaci krotki
        :param amt_of_specific: button tworzący instancję klasy i tworzący krotkę ilość maszyn
        """

        #Labels
        self.label_types = tk.Label(self.root, text='Enter number of types:').place(x=5, y=120)

        self.label_amt_tom = tk.Label(self.root, text='Enter amount of machines:').place(x=205, y=120)

        #Entries
        self.entry_types = tk.Entry(self.root).place(x=5, y=140, width=50)

        self.entry_amt_tom = tk.Entry(self.root).place(x=205, y=140)

        #Buttons
        self.amt_of_specific = tk.Button(self.root, text = 'Set Machines instance', relief=tk.RAISED, command=self.amt_of_specific_type).place(x=5, y=165)


        #Trzecia część modyfikowalna - utworzenie instancji klasy Product
        """
        :param label_amt_products/entry_amt_products: label oraz wprowadzenie ilosci produktow
        :param label_index/entry_index: label oraz wprowadzenie obecnie modyfikowanego produktu
        :param label_profit/entry_profit: label oraz wprowadzenie zysku z danego produktu
        :param label_hps/entry_hps: label oraz wprowadzenie godzin potrzebnych na poszczegolnym etapie produkcji do wytworzenia produktu danego rodzaju
        :param button_amt_products: przycisk resetujacy wczesniejsze ustawienia, tworzacy nowe zerowe listy
        :param button_product_index: przycisk tworzacy produkt o zadanym indeksie
        :param button_create_hps_matrix: przycisk tworzacy macierz hps, po utworzeniu wczesniejszym produktow
        """

        #Labels
        self.label_amt_products = tk.Label(self.root, text='Enter number of products:').place(x=5, y=200)

        self.label_index = tk.Label(self.root, text='Enter index of product u want to edit:').place(x=205, y=200)

        self.label_profit = tk.Label(self.root, text='Enter generated profit from product:').place(x=405, y=200)

        self.label_hps = tk.Label(self.root, text='Enter hours per stage:').place(x=605, y=200)

        #Entries
        self.entry_amt_products = tk.Entry(self.root).place(x=5, y=220, width=50)

        self.entry_index = tk.Entry(self.root).place(x=205, y=220, width=50)
        
        self.entry_profit = tk.Entry(self.root).place(x=405, y=220, width=50)
        
        self.entry_hps = tk.Entry(self.root).place(x=605, y=220)

        #Buttons
        self.button_amt_products = tk.Button(self.root, text='Confirm amount of products', command=self.create_amt_products).place(x=5, y=245)

        self.button_product_index = tk.Button(self.root, text='Create product', relief=tk.RAISED, command=self.create_product).place(x=405, y=245)

        self.button_create_hps_matrix = tk.Button(self.root, text='Create hps matrix', relief=tk.RAISED, command=self.create_hps_matrix).place(x=605, y=245)


        #Sposób usuwania - mozliwa modyfikacja
        """
        :param checkButton_default_deletion: mozliwosc wlaczenia losowego usuwania elementów
        :param checkButton_deterministic_deletion: mozliwosc wlaczenia deterministycznego usuwania elementow
        """

        self.checkButton_default_deletion = tk.Checkbutton(self.root, text='Random deletion of elements', variable=self.default_deletion, onvalue=1, offvalue=0, command=self.choose_deletion_type).place(x=5, y=275)

        self.checkButton_deterministic_deletion = tk.Checkbutton(self.root, text='Deterministic deletion of elements', variable=self.deterministic_deletion, onvalue=1, offvalue=0, command=self.choose_deletion_type).place(x=305, y=275)


        #Wybor sposobu dobierania sasiedztwa - mozliwa modyfikacja
        """
        :param checkButton_default_neigh: mozliwosc wlaczenie losowego doboru sasiedztwa
        :param checkButton_detereministic_neigh: mozliwosc wlaczenia deterministycznego doboru sasiedztwa
        """

        self.checkButton_default_neigh = tk.Checkbutton(self.root, text='Random neighbours', variable=self.default_neigh, onvalue=1, offvalue=0, command=self.choose_neigh).place(x=5, y=295)
        
        self.checkButton_deterministic_neigh = tk.Checkbutton(self.root, text='Deterministic neighbours', variable=self.deterministic_neigh, onvalue=1, offvalue=0, command=self.choose_neigh).place(x=305, y=295)


        #Kryterium aspiracji - mozliwa modyfikacja
        """
        :param checkButton_default_aspiration: mozliwosc wlaczenia randomowego kryterium aspiracji
        :param checkButton_one_of_best_aspiration: mozliwosc wlaczenia wyboru jednego z najlepszych rozwiazan wczesniejszych
        """

        self.checkButton_default_aspiration = tk.Checkbutton(self.root, text='Random Aspiration Cirteria', variable=self.default_aspiration, onvalue=1, offvalue=0, command=self.aspiration_criteria).place(x=5, y=315)

        self.checkButton_one_of_best_aspiration = tk.Checkbutton(self.root, text='One of best Aspiration Cirteria', variable=self.one_of_best_aspiration, onvalue=1, offvalue=0, command=self.aspiration_criteria).place(x=305, y=315)

        
        #Tabu search - mozliwa modyfikacja
        """
        :param checkButton_default_tabu_search: mozliwosc zmiany listy tabu na stala dlugosc
        :param checkButton_deterministic_tabu_search: mozliwosc zmianny na zmienna dlugosc listy tabu
        """

        self.checkButton_default_tabu_search = tk.Checkbutton(self.root, text='Constant length of tabu list', variable=self.default_ts, onvalue=1, offvalue=0, command=self.ts_check).place(x=5, y=335)

        self.checkButton_deterministic_tabu_search = tk.Checkbutton(self.root, text='Deterministic length of tabu list', variable=self.deterministic_ts, onvalue=1, offvalue=0, command=self.ts_check).place(x=305, y=335)


        #Utworzenie rozwiazania
        """
        :param button_create_solution: utworzenie pierwszego rozwiazania
        """

        self.button_create_solution = tk.Button(self.root, text='Create solution', relief=tk.RAISED, command=self.create_solution).place(x=5, y=365)


        #Max iter i aspiration threshold - mozliwa modyfikacja

        """
        :param label_max_iter/entry_max_iter: mozliwosc zmiany maksymalnej ilosci iteracji
        :param label_threshold/entry_threshold: mozliwosc zmiany threshold
        :param button_confirm: zamiana wartosci max_iter oraz threshold
        """

        #Labels
        self.label_max_iter = tk.Label(self.root, text='Enter max iter:').place(x=5, y=395)

        self.label_threshold = tk.Label(self.root, text='Enter threshold:').place(x=205, y=395)

        #Entries
        self.entry_max_iter = tk.Entry(self.root).place(x=5, y=415, width=50)

        self.entry_threshold = tk.Entry(self.root).place(x=205, y=415, width=50)

        #Buttons
        self.button_confirm = tk.Button(self.root, text='Confirm', relief=tk.RAISED, command=self.iter_thresh).place(x=605, y=415)


        #Uruchomienie algorytmu
        """
        :param button_algorithm_ts: poszukiwanie rozwiazania algorytmem
        """

        self.button_algorithm_ts = tk.Button(self.root, text='Run algorithm', relief=tk.RAISED, command=self.run_algorithm).place(x=5, y=455)


        #Uruchomienie wykresów
        """
        :param button_show_plot: wyswietlanie wykresu
        """

        self.button_show_plot = tk.Button(self.root, text='Show plot', relief=tk.RAISED, command=self.show_plot).place(x=605, y=455)


        #Wyswietlenie wartosci wyniku dzialania algorytmu
        self.text = tk.Label(self.root, text='Your algorithm result:').place(x=5, y=495)

        self.root.mainloop()


    def new_window(self):
        window = tk.Toplevel()
        window.title("Show data")
        window.geometry("800x600")
        window.resizable(width=False, height=False)

        ico = Image.open('ikona.jpg')
        photo = ImageTk.PhotoImage(ico)
        window.wm_iconphoto(False, photo)

        self.button_close = tk.Button(window, text='Close window', relief=tk.RAISED, command=window.destroy).place(x=710, y=5)


    def load_from_file(self):
        Tk().withdraw()
        filename = askopenfilename()

        with open(f'{filename}') as f:
            lines = f.read().splitlines()
            
            worker_line = lines[0]
            machines_line = lines[1]
            products_line = lines[2:]

            f.close()

        worker_line = worker_line.split(sep=':')
        machines_line = machines_line.split(sep=':')
       
        for idx in range(len(products_line)):
            products_line[idx] = products_line[idx].split(sep=':')

        #Worker
        amt_worker, check_time, dow, hpd = tuple(worker_line)
        self.worker = Workers(int(amt_worker), int(check_time), int(dow), int(hpd))
        self.wrk_hrs = self.worker.worker_hours()

        #Machines
        machine_types, amt_machine_types = tuple(machines_line)
        self.mach = Machines(int(machine_types))

        amt_machine_types = amt_machine_types.split(sep=',')

        for idx in range(len(amt_machine_types)):
            amt_machine_types[idx] = int(amt_machine_types[idx])

        self.amt_tuple = self.mach.amount_of_specific_type(amt_machine_types)

        #Products
        length_pl = len(products_line)

        self.profits = [0 for _ in range(length_pl)]
        self.hps_matrix = [0 for _ in range(length_pl)]
        for idx in range(length_pl):
            self.profits[idx] = int(products_line[idx][0])

        hps = [0 for _ in range(length_pl)]
        for idx in range(length_pl):
            hps[idx] = products_line[idx][1].split(sep=',')
            self.hps_matrix[idx] = [int(x) for x in hps[idx]]
        
        self.hps_matrix = np.column_stack(self.hps_matrix)

    def save_to_file(self):
        pass #TODO: do zrobienia jeszcze zapisywanie


    def get_number_of_workers(self):
        try:
            amt = int(self.entry_worker.get())
            ct = int(self.entry_ct.get())

            if len(self.entry_dow.get()) == 0 and len(self.entry_hpd.get()) == 0: 
                self.worker = Workers(amt, ct)
            elif len(self.entry_dow.get()) == 0 or len(self.entry_hpd.get()) == 0:
                if len(self.entry_hpd.get()) == 0:
                    dow = int(self.entry_dow.get())
                    self.worker = Workers(amt, ct, dow)
                else:
                    hpd = int(self.entry_hpd.get())
                    self.worker = Workers(amt, ct, hours_per_day=hpd)
            else:
                dow = int(self.entry_dow.get())
                hpd = int(self.entry_hpd.get())
                self.worker = Workers(amt, ct, dow, hpd)

            self.wrk_hrs = self.worker.worker_hours()

        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


    def amt_of_specific_type(self):
        try:
            types = int(self.entry_types.get())
            self.mach = Machines(types)

            amt = self.entry_amt_tom.get().split(sep=',')
            for i in range(len(amt)):
                amt[i] = int(amt[i])
            
            if self.mach.types != len(amt):
                messagebox.showinfo(title='Error', message='The amount of types is not equal to kind of types!')    

            self.amt_tuple = self.mach.amount_of_specific_type(amt)
        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


    def create_amt_products(self):
        try:
            amount = int(self.entry_amt_products.get())

            self.amt_products = [0 for _ in range(amount)]
            self.profits = [0 for _ in range(amount)]
            self.hps_matrix = [0 for _ in range(amount)]
        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


    def create_product(self):
        try:
            index = int(self.entry_index.get())
            profit = int(self.entry_profit.get())
            types = self.mach.types
            self.prod = Product(profit, types)

            time_required = self.entry_hps.get().split(sep=',')

            if index < 1 or index > int(self.entry_amt_products.get()):
                messagebox.showinfo(title='Warning', message='Index is out of created range!')

            for i in range(len(time_required)):
                time_required[i] = int(time_required[i])

            if len(time_required) != self.prod.amount_of_mt:
                messagebox.showinfo(title='Error', message='The amount of types is not equal to kind of types!')

            self.profits[index-1] = profit
            self.hps_matrix[index-1] = time_required         
        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


    def create_hps_matrix(self):
        self.prod = Product(1, self.mach.types)

        for index in range(len(self.hps_matrix)):
            self.hps_matrix[index] = np.transpose(self.hps_matrix[index])

        self.hps_matrix = np.column_stack(self.hps_matrix)


    def ts_check(self):
        if self.default_ts.get() == self.deterministic_ts.get() and (self.deterministic_ts.get() == 1 or self.deterministic_ts.get() == 0):
            pass
        elif self.default_ts.get() == 1:
            self.ts = 'constant'
        elif self.deterministic_ts.get() == 1:
            self.ts = 'deterministic'


    def aspiration_criteria(self):
        if self.default_aspiration.get() == self.one_of_best_aspiration.get() and (self.default_aspiration.get() == 1 or self.default_aspiration.get() == 0):
            pass
        elif self.default_aspiration.get() == 1:
            self.aspiration = 'random'
        elif self.one_of_best_aspiration.get() == 1:
            self.aspiration = 'random_best'


    def choose_neigh(self):
        if self.default_neigh.get() == self.deterministic_neigh.get() and (self.default_neigh.get() == 1 or self.default_neigh.get() == 0):
            pass
        elif self.default_neigh.get() == 1:
            self.neigh_type = 'default'
        elif self.deterministic_neigh.get() == 1:
            self.neigh_type = 'deterministic'


    def choose_deletion_type(self):
        if self.default_deletion.get() == self.deterministic_deletion.get() and (self.default_deletion.get() == 1 or self.default_deletion.get() == 0):
            pass
        elif self.default_deletion.get() == 1:
            self.del_selection = 'default'
        elif self.deterministic_deletion.get() == 1:
            self.del_selection = 'deterministic'


    def iter_thresh(self):
        try:
            self.max_iter = int(self.entry_max_iter.get())
            self.threshold = int(self.entry_threshold.get())
        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


    def create_solution(self):
        self.sol = Solution(hours_per_stage=self.hps_matrix, profit=self.profits, machines_per_stage=self.amt_tuple, checking_time=self.worker.checking_time, worker_hours=self.wrk_hrs, days_of_work=self.worker.days_of_work, hours_per_day=self.worker.hours_per_day)
        self.sol.random_solution()


    def run_algorithm(self):
        if self.default_aspiration.get() == self.one_of_best_aspiration.get() and self.one_of_best_aspiration.get() == 1:
            messagebox.showinfo(title='Warning', message='Both types of criteria aspiration are active!')
        elif self.default_aspiration.get() == self.one_of_best_aspiration.get() and self.one_of_best_aspiration.get() == 0:
            messagebox.showinfo(title='Warning', message='None of types of criteria aspiration is active!')

        if self.default_neigh.get() == self.deterministic_neigh.get() and self.deterministic_neigh.get() == 1:
            messagebox.showinfo(title='Warning', message='Both types of neighbour type are active!')
        elif self.default_neigh.get() == self.deterministic_neigh.get() and self.deterministic_neigh.get() == 0:
            messagebox.showinfo(title='Warning', message='None of types of neighbour type is active!')

        if self.default_deletion.get() == self.deterministic_deletion.get() and self.deterministic_deletion.get() == 1:
            messagebox.showinfo(title='Warning', message='Both types of deletion type are active!')
        elif self.default_deletion.get() == self.deterministic_deletion.get() and self.deterministic_deletion.get() == 0:
            messagebox.showinfo(title='Warning', message='None of types of deletion type is active!')

        if self.sol == []:
            messagebox.showinfo(title='Warning', message='No solution found yet!')
        else:
            ts = TabuSearch(solution=self.sol, neigh_type=self.neigh_type, aspiration_criteria=self.aspiration, max_iter=self.max_iter, aspiration_threshold=self.threshold)
            self.text['text'] = ts.algorythm()


    def show_plot(self):
        pass #TODO: dodanie logiki do tworzenia wykresow

Gui()