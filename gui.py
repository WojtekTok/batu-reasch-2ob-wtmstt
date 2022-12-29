from main import *
import tkinter as tk
from tkinter import messagebox

#Zdefiniowanie parametrów wejściowych w celu ich zmiany

#Zdefiniowanie pracowników
worker = Workers(10, 10)

#Zdefiniowanie ilości maszyn
mach = Machines(3)
mpt = mach.amount_of_specific_type([3, 3, 2])

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

class Gui():

    # #Zdefiniowanie pracowników
    # worker = Workers(10, 10)

    # #Zdefiniowanie ilości maszyn
    # mach = Machines(3)

    def __init__(self):
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

        self.label_worker = tk.Label(self.root, text='Enter the number of workers:')
        self.label_worker.grid(row=0, column=0)

        self.label_ct = tk.Label(self.root, text='Enter time required to check time:')
        self.label_ct.grid(row=0, column=1)

        self.label_dow = tk.Label(self.root, text='Enter days of work:')
        self.label_dow.grid(row=0, column=2)

        self.label_hpd = tk.Label(self.root, text='Enter hours per day:')
        self.label_hpd.grid(row=0, column=3)

        self.entry_worker = tk.Entry(self.root)
        self.entry_worker.grid(row=1, column=0)

        self.entry_ct = tk.Entry(self.root)
        self.entry_ct.grid(row=1, column=1)

        self.entry_dow = tk.Entry(self.root)
        self.entry_dow.grid(row=1, column=2)

        self.entry_hpd = tk.Entry(self.root)
        self.entry_hpd.grid(row=1, column=3)

        self.set_workers_button = tk.Button(self.root, text = 'Set Workers instance', relief=tk.RAISED, command=self.get_number_of_workers)
        self.set_workers_button.grid(row=2, column=0, sticky=tk.E+tk.W)


        #Utworzenie instancji klasy Machines
        self.label_types = tk.Label(self.root, text='Enter number of types:')
        self.label_types.grid(row=3, column=0)

        self.label_amt_tom = tk.Label(self.root, text='Enter amount of machines[pattern: "3,5,6"]:')
        self.label_amt_tom.grid(row=3, column=1)

        self.entry_types = tk.Entry(self.root)
        self.entry_types.grid(row=4, column=0)

        self.entry_amt_tom = tk.Entry(self.root)
        self.entry_amt_tom.grid(row=4, column=1)

        self.amt_of_specific = tk.Button(self.root, text = 'Set Machines instance', relief=tk.RAISED, command=self.amt_of_specific_type)
        self.amt_of_specific.grid(row=5, column=0)

        self.root.mainloop()

    def get_number_of_workers(self):
        try:
            amt = int(self.entry_workers.get())
            ct = int(self.entry_ct.get())

            if len(self.entry_dow.get()) == 0 and len(self.entry_hpd.get()) == 0: 
                worker = Workers(amt, ct)
            elif len(self.entry_dow.get()) == 0 or len(self.entry_hpd.get()) == 0:
                if len(self.entry_hpd.get()) == 0:
                    dow = int(self.entry_dow.get())
                    worker = Workers(amt, ct, dow)
                else:
                    hpd = int(self.entry_hpd.get())
                    worker = Workers(amt, ct, hours_per_day=hpd)
            else:
                dow = int(self.entry_dow.get())
                hpd = int(self.entry_hpd.get())
                worker = Workers(amt, ct, dow, hpd)

        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')

    def amt_of_specific_type(self):
        try:
            types = int(self.entry_types.get())
            mach = Machines(types)

            amt = self.entry_amt_tom.get().split(sep=',')
            for i in range(len(amt)):
                amt[i] = int(amt[i])
            
            amt_tuple = mach.amount_of_specific_type(amt)
        except:
            messagebox.showinfo(title='Error', message='Please enter valid number!')


Gui()