"""

"""
import numpy as np
import time
import csv

class Sudoku_m:

    def __init__(self):
        self.table = np.zeros((9, 9))
        self.matchs = 0
        self.numbers_matched = {}
        self.loops = 0

    def innitalizer(self):
        inicio = time.time()
        #############################
        """
        Atualmente a lógica do programa somente aceita sudoku's que são de nivel normal <
        """
        filename = "sudoku_file_normal.csv"
        #############################
        self.open_a_csvfile(filename)
        value = 0
        while self.matchs < 81 and self.loops < 81:
            self.loops += 1
            value += 1
            self.validade_checks(value)
            if value == 9:
                value = 0

        self.print_table(self.table);
        fim = time.time()
        print("tempo de execução: " + str(fim - inicio))

    def validade_checks(self, value):
        table_aux = np.zeros((9, 9))
        for line in range(9):
            for column in range(9):
                if not self.table[line, column] == 0:
                    table_aux[line, column] = 1
                    if self.table[line, column] == value:
                        table_aux = self.fill_aux_table(table_aux, line, column)

        for line in range(9):
            for column in range(9):
                if table_aux[line, column] == 0:
                    if self.valid_value(table_aux, line, column):
                        table_aux[line, column] = 1
                        self.fill_aux_table(table_aux, line, column)
                        self.table[line, column] = value
                        self.matchs += 1;
                        print("Value "+str(value)+" on ["+str(line+1)+", "+str(column+1)+"]")

    def valid_value(self, table_aux, line, column):
        check_line = False
        check_column = False
        probaly_valid_value = True
        aux_line = int(line / 3) * 3
        aux_column = int(column / 3) * 3
        for i in range(aux_line, (aux_line + 3)):
            for j in range(aux_column, (aux_column + 3)):
                if not (line == i and column == j) and table_aux[i, j] == 0:
                    check_line = True
                    break
            if check_line:
                break
        if check_line:
            for i in range(9):
                if not line == i and table_aux[i, column] == 0:
                    check_column = True
                    break
        if check_column:
            for i in range(9):
                if not column == i and table_aux[line, i] == 0:
                    probaly_valid_value = False
                    break
        return probaly_valid_value

    def fill_aux_table(self, table_aux, line, column):
        for i in range(9):
            table_aux[line, i] = 1
            table_aux[i, column] = 1
        aux_line = int(line / 3) * 3
        aux_column = int(column / 3) * 3

        for i in range(aux_line, aux_line + 3):
            for j in range(aux_column, aux_column + 3):
                table_aux[i, j] = 1

        return table_aux

    def print_table(self, table):
        for i in range(9):
            print("[", end='')
            for j in range(9):
                print(str(table[i, j]) + " ", end='')
            print("]")

    def open_a_csvfile(self, filename):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            line = 0
            for row in reader:
                print(row)
                for column in range(9):
                    if row[column] == '':
                        value = 0
                    else:
                        value = int(row[column])
                        self.matchs += 1
                    self.table[line, column] = value
                line += 1

    def main(self):
        self.innitalizer()


if __name__ == "__main__":
    maker = Sudoku_m()
    maker.main()
