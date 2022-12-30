from main import *
import tkinter as tk
from tkinter import messagebox

class Gui():

    def __init__(self, worker=Workers(1,1), mach=Machines(1), prod=Product(1,1), amt_tuple=0, amt_products = [], profits = [], hps_matrix = []):
        """
        Zdefiniowanie zmiennych tak, żeby mieć do nich dostęp w całej klasie
        :param worker: instancja klasy Workers
        :param mach: instancja klasy Machines
        :param prod: instancja klasy Product
        :param amt_tuple: amount of types, krotka zawierająca ilość maszyn danego rodzaju
        :param amt_products: amount of products, lista zawierająca informację o produktach
        :param profits: lista zawierająca zysk z poszczególnych produktów
        :param hps_matrix: macierz zawierająca czas potrzebny na wykonanie produktów na poszczególnym etapie
        """
        self.worker = worker
        self.mach = mach
        self.prod = prod
        self.amt_tuple = amt_tuple
        self.amt_products = amt_products
        self.profits = profits
        self.hps_matrix = hps_matrix

        #GUI
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)

        #Konfiguracja układu GUI
        self.root.rowconfigure(0, weight=3)
        self.root.columnconfigure([0,1,2,3], weight=3)


        #Pierwsza część modyfikowalna - utworzenie instancji klasy Workers
        """
        :param label_worker/entry_worker: label oraz wprowadzenie ilości pracowników
        :param label_ct/entry_ct: label oraz wprowadzenie wartosci checking_time (w godzinach)
        :param label_dow/entry_dow: label oraz wprowadzenie wartości dni pracy w tygodniu (nieobowiązkowe)
        :param label_hpd/entry_hpd: label oraz wprowadzenie wartości godzin pracy w ciągu dnia (nieobowiązkowe)
        :param set_workers_button: umożliwia utworzenie instancji klasy Workers z ustawionymi parametrami
        """

        #Labels
        self.label_worker = tk.Label(self.root, text='Enter the number of workers:')
        self.label_worker.grid(row=0, column=0)

        self.label_ct = tk.Label(self.root, text='Enter time required to check time:')
        self.label_ct.grid(row=0, column=1)

        self.label_dow = tk.Label(self.root, text='Enter days of work:')
        self.label_dow.grid(row=0, column=2)

        self.label_hpd = tk.Label(self.root, text='Enter hours per day:')
        self.label_hpd.grid(row=0, column=3)

        #Entries
        self.entry_worker = tk.Entry(self.root)
        self.entry_worker.grid(row=1, column=0)

        self.entry_ct = tk.Entry(self.root)
        self.entry_ct.grid(row=1, column=1)

        self.entry_dow = tk.Entry(self.root)
        self.entry_dow.grid(row=1, column=2)

        self.entry_hpd = tk.Entry(self.root)
        self.entry_hpd.grid(row=1, column=3)

        #Buttons
        self.set_workers_button = tk.Button(self.root, text = 'Set Workers instance', relief=tk.RAISED, command=self.get_number_of_workers)
        self.set_workers_button.grid(row=2, column=0, sticky=tk.E+tk.W)


        #Druga część modyfikowalna - utworzenie instancji klasy Machines
        """
        :param label_types/entry_types: label oraz wprowadzenie ilości rodzajów maszyn na produkcji
        :param label_amt_tom/entry_amt_tom: label oraz wprowadzenie (amount_types_of_machines) ilość maszyn danego rodzaju w postaci krotki
        :param amt_of_specific: button tworzący instancję klasy i tworzący krotkę ilość maszyn
        """

        #Labels
        self.label_types = tk.Label(self.root, text='Enter number of types:')
        self.label_types.grid(row=3, column=0)

        self.label_amt_tom = tk.Label(self.root, text='Enter amount of machines[pattern: "3,5,6"]:')
        self.label_amt_tom.grid(row=3, column=1)

        #Entries
        self.entry_types = tk.Entry(self.root)
        self.entry_types.grid(row=4, column=0)

        self.entry_amt_tom = tk.Entry(self.root)
        self.entry_amt_tom.grid(row=4, column=1)

        #Buttons
        self.amt_of_specific = tk.Button(self.root, text = 'Set Machines instance', relief=tk.RAISED, command=self.amt_of_specific_type)
        self.amt_of_specific.grid(row=5, column=0)

        #Trzecia część modyfikowalna - utworzenie instancji klasy Product
        """
        
        """

        #Labels
        self.label_amt_products = tk.Label(self.root, text='Enter number of products:')
        self.label_amt_products.grid(row=6, column=0)

        self.label_index = tk.Label(self.root, text='Enter index of product u want to edit:')
        self.label_index.grid(row=6, column=1)

        self.label_profit = tk.Label(self.root, text='Enter generated profit from product:')
        self.label_profit.grid(row=6, column=2)

        self.label_hps = tk.Label(self.root, text='Enter hours per stage:')
        self.label_hps.grid(row=6, column=3)

        #Entries
        self.entry_amt_products = tk.Entry(self.root)
        self.entry_amt_products.grid(row=7, column=0)

        self.entry_index = tk.Entry(self.root)
        self.entry_index.grid(row=7, column=1)
        
        self.entry_profit = tk.Entry(self.root)
        self.entry_profit.grid(row=7,  column=2)
        
        self.entry_hps = tk.Entry(self.root)
        self.entry_hps.grid(row=7, column=3)

        #Buttons
        self.button_amt_products = tk.Button(self.root, text='Confirm amount of products', command=self.create_amt_products)
        self.button_amt_products.grid(row=8, column=0)

        self.button_product_index = tk.Button(self.root, text='Create product', relief=tk.RAISED, command=self.create_product)
        self.button_product_index.grid(row=8, column=2)

        self.root.mainloop()

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

            print(self.profits)
            print(self.hps_matrix)            

        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')

Gui()