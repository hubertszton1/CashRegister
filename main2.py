import glob
import os
import re
from datetime import date, datetime
import matplotlib.pyplot as plt
from colorama import Fore, Style
from prettytable import PrettyTable

try:
    today = date.today()
    files_path = os.path.expanduser("~/Documents/files/")
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    files = glob.glob(files_path+"*.txt")
    files.sort(key=lambda x: -os.path.getmtime(x))
    last_time = datetime.fromtimestamp(os.path.getmtime(files[0]))
except IndexError:
    pass


class CashRegister:

    def __init__(self):
        self.sale = [0]
        self.daily_income = [0]
        self.time = [datetime.now().strftime("%H:%M")]

        # Program próbuje wczytać miesięczny zysk i ilość pieniędzy w kasie
        # Jeżeli się nie uda, program zapyta ile pieniędzy jest aktualnie w kasie
        # A miesięczny zysk zostanie wyzerowany
        try:
            with open(files[0], 'r') as file:
                lines = file.readlines()
                data = lines[1].strip().split('\t')
                self.in_till = [float(data[3])]
                if last_time.month == today.month:
                    self.monthly_income = [float(data[4])]
                else:
                    self.monthly_income = [0]
        except (FileNotFoundError, IndexError):
            self.in_till = [float(input("W kasie: "))]
            self.monthly_income = [0]

        # zmienne, które tymczasowo przechowują wartości usunięte za pomocą komendy "back"
        self.time_tmp = None
        self.monthly_income_tmp = None
        self.in_till_tmp = None
        self.daily_income_tmp = None
        self.sale_tmp = None

        # table przechowuje objekt utwożony przy pomocy klasy PrettyTable
        self.table = None

    def insert(self, sale):
        self.sale.append(sale)
        self.daily_income.append(sum(self.sale))
        self.in_till.append(self.in_till[-1] + sale)
        self.monthly_income.append(self.monthly_income[-1] + sale)
        self.time.append(datetime.now().strftime("%H:%M"))

    def view(self):
        self.table = PrettyTable()

        # pokoloruj ostatni wiersz
        sale_before = self.sale[-1]
        self.sale[-1] = f"{Fore.GREEN}{self.sale[-1]:.2f}{Style.RESET_ALL}"
        daily_income_before = self.daily_income[-1]
        self.daily_income[-1] = f"{Fore.GREEN}{self.daily_income[-1]:.2f}{Style.RESET_ALL}"
        in_till_before = self.in_till[-1]
        self.in_till[-1] = f"{Fore.GREEN}{self.in_till[-1]:.2f}{Style.RESET_ALL}"
        time_before = self.time[-1]
        self.time[-1] = f"{Fore.GREEN}{self.time[-1]}{Style.RESET_ALL}"
        monthly_income_before = self.monthly_income[-1]
        self.monthly_income[-1] = f"{Fore.GREEN}{self.monthly_income[-1]:.2f}{Style.RESET_ALL}"

        # utwórz tabele
        self.table.add_column("Sprzedane", self.sale)
        self.table.add_column("Zysk", self.daily_income)
        self.table.add_column("W kasie", self.in_till)
        self.table.add_column("W miesiacu", self.monthly_income)
        self.table.add_column("Godzina", self.time)

        # zresetuj wszystko po utworzeniu tabeli
        self.sale[-1] = sale_before
        self.daily_income[-1] = daily_income_before
        self.in_till[-1] = in_till_before
        self.time[-1] = time_before
        self.monthly_income[-1] = monthly_income_before

        # wyprintuj tabelę
        os.system("clear")
        self.table.align = "c"
        self.table.float_format = ".2"
        print(self.table)

    def back(self):
        if len(self.sale) <= 1:
            raise ValueError
        self.sale_tmp = self.sale.pop()
        self.daily_income_tmp = self.daily_income.pop()
        self.in_till_tmp = self.in_till.pop()
        self.monthly_income_tmp = self.monthly_income.pop()
        self.time_tmp = self.time.pop()

    def forward(self):
        self.sale.append(self.sale_tmp)
        self.daily_income.append(self.daily_income_tmp)
        self.in_till.append(self.in_till_tmp)
        self.monthly_income.append(self.monthly_income_tmp)
        self.time.append(self.time_tmp)
        del self.sale_tmp
        del self.daily_income_tmp
        del self.in_till_tmp
        del self.monthly_income_tmp
        del self.time_tmp

    def quit(self):
        now = datetime.now()
        file_name = now.strftime("%d %B %Y, %H-%M")
        fieldnames = ['Godzina', 'Sprzedaz', 'Zysk_dnia', 'W_kasie', 'W_miesiacu']
        with open(files_path + file_name + ".txt", 'w') as file:
            file.write(f"{fieldnames[0]:8}\t"
                       f"{fieldnames[1]:8}\t"
                       f"{fieldnames[2]:8}\t"
                       f"{fieldnames[3]:8}\t"
                       f"{fieldnames[4]:8}\n")

            file.write(f"{self.time[0]:<8}\t"
                       f"{self.sale[0]:<8.2f}\t"
                       f"{self.daily_income[-1]:<8.2f}\t"
                       f"{self.in_till[-1]:<8.2f}\t"
                       f"{self.monthly_income[-1]:<8.2f}\n")

            for i in range(len(self.sale) - 1):
                file.write(f"{self.time[i + 1]:<8}\t{self.sale[i + 1]:<8.2f}\n")

        print(f"{Fore.GREEN}Program został zamknięty{Style.RESET_ALL}")


##########################
###### MAIN PROGRAM ######
##########################
def main():
    cash_reg = CashRegister()

    while True:
        cash_reg.view()
        try:
            insert = input("Wprowadz: ").strip()
            if insert == "back":
                cash_reg.back()
            elif insert == "graph":
                cash_reg.graph()
            elif insert == "for":
                cash_reg.forward()
            elif insert == "quit":
                cash_reg.quit()
                exit()
            elif matches := re.search(r"^(-?[0-9]+(\.[0-9][0-9]?)?) -kasa$", insert, re.IGNORECASE):
                cash_reg.in_till[-1] += float(matches.group(1))
            else:
                sale = float(insert)
                cash_reg.insert(sale)
        except (ValueError, IndexError, AttributeError, TypeError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    main()
