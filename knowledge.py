# Classe responsável por armazenar as informações de regras e dados do jogo
import csv
import copy

class knowledge:

    def head(self):
        """
        Regras do jogo:
        (1) - Em casa quadrado, linha e coluna somente deve haver somente um exemplar de cada número
            ex: Casa A1 = 1, então em todos A~'s e ~1's e na região que ele se encontra não devem haver outro 1
        (2) - 
        """
        self.lines = "123456789" # números de linhas
        self.columns = "ABCDEFGHI" # número de colunas
        #### FILE NAME ####
        file = "sudoku_file_world_hardest.csv"
        ####################
        cells = self.create_table() 
        self.crosses = self.crosses_groups()
        self.cells_p = dict({cell: self.find_intersection(cell) for cell in cells}) 
        table_values = dict(zip(cells, self.open_csvfile(file)))
        self.print_table(table_values)
        print("+" * 21)
        for key, value in table_values.items():
            if value == 0:
                possibilities = [table_values[item] for item in self.cells_p[key] if table_values[item] != 0 and not type(table_values[item]) is list]
                value = [number for number in '123456789' if number not in possibilities]
                table_values[key] = sorted(set(value))

        table_values, is_stuck, total = self.basic_instance(table_values)
        self.print_table(table_values)

    def print_table(self, complete_table):
        for key, value in complete_table.items():
            print("{} ".format(value), end='')
            if key.endswith(('3', '6')):
                print("| ", end = '')
            elif key.endswith('9'):
                print('\n', end='')
            if key in ['C9', 'F9']:
                print("-" * 21)

    def basic_instance(self, table_values):
        """ Método de instancia. Este tenta aplicar as regras para a tabela em sua mão, e em caso de travamento,
            irá gerar várias instancias que irão executar a mesma tarefa a partir de um valor presumido(arriscado).
            * os valores são selecionados em ordem
            """
        local_table, is_stuck, total = self.instance_workbench(table_values)
        if is_stuck:
            for key, value in local_table.items():
                if type(value) is list:
                    for item in local_table[key]:
                        test_table_values = copy.deepcopy(local_table) # Cria um Backup da tabela original
                        test_table_values[key] = [item] # arrisca o valor á ordem na sua lista de possiblidades
                        local_instance, local_stuck, local_total = self.basic_instance(test_table_values)
                        if local_total == 81:
                            return local_instance, False, local_total # Caso a isntancia chegue a tabela verdadeira, retornar imediatamente
                    return local_instance, False, 0
        else:
            return local_table, False, total

    def instance_workbench(self, local_table):
        """ 'Mesa de trabalho' do programa, aonde o codigo aplica as regras que lhe foram 'ensinadas' do sudoku. 
            Repetirá até chegar em um dos estados de:
            - Total alcançado: 81 itens encontrados(Sudoku completo)
            - Travado: Encontrado somente células com duas ou mais possibilidades de valores.
                OU
            - Caso a instancia local chegue a uma solução impossível(células sem possibilidades de inserção)
        Parametros:
            local_table: dict com todos valores e possibilidades da tabela a mão da instancia
        Retornos:
            local_table: dict com todos os valores e posbilidades após a aplicação das regras
                *Lembrando que é retorna a tabela completa OU não
            is_stuck: estado bool de instancia travada ou não
            total: número alcançado de valores únicos em células
        """
        while True: # Repetirá enquanto a instancia não entrar no estado de 'Travado'
            total = 0
            is_stuck = True
            for key, value in local_table.items():
                if type(value) is list:
                    if len(value) == 0: # Caso de falha crítica, este segmento está incorreto
                        return local_table, False, 0 # Caso o codigo encontre alguma célula sem valor algum, e sem possibilidades de inserção
                    elif len(value) == 1: # Caso que estamos esperando, com somente uma possibilidade de interseção(MATCH)
                        is_stuck = False
                        local_table = self.remove_possibilities(local_table, key, value) # REGRA 1
                        local_table[key] = value[0] # Insere naquela posição o valor encontrado
                    else:
                        for cross in self.crosses: # REGRA2
                            if key in cross:
                                test_value = value
                                for cell in cross:
                                    test_value = set(test_value) - set(local_table[cell]) if cell != key else test_value
                                    if len(test_value) == 0:
                                        break
                                if len(test_value) == 1: # Caso procurado pela REGRA 2
                                    is_stuck = False
                                    local_table[key] = sorted(test_value) # Formata para ser encontrado pel acondição REGRA 1
                                    break
                else:
                    total += 1
            if not local_table or not total < 81 or is_stuck:
                break
        is_stuck = False if total == 81 else is_stuck
        return local_table, is_stuck, total
        
    def remove_possibilities(self, table, key, inserted_value):
        """ Descarta da lista de todas as 'células' sobre influência Regra 1 desta célula via parametro. """
        for cell in self.cells_p[key]:
            table[cell] = sorted(set(table[cell]) - set(inserted_value)) if type(table[cell]) is list else table[cell]
        return table

    def create_table(self):
        """ Cria a tabela no estilo Batalha Naval. - A1 ~ I9 [9x9] """
        return [column + line for column in self.columns for line in self.lines]

    def find_intersection(self, cell):
        """ Procura e adiciona em uma lista todas interseções de cada célula. """
        contacts = sum((cross for cross in self.crosses if cell in cross), [])
        return sorted(set(contacts) - set([cell]))

    def crosses_groups(self):
        """ Lista contendo todas possibilidades de interseção no programa. (linhas, colunas e quadrados). """
        lines = [self.cross(self.columns, l) for l in self.lines]
        cols = [self.cross(c, self.lines) for c in self.columns]
        squares = [self.cross(col, line) for line in ('123','456','789') for col in ('ABC', 'DEF', 'GHI')]
        return lines + cols + squares
        
    def cross(self, x, y):
        """ Realiza a busca de todos os elementos determinados pela entrada. """
        return [x1 + y1 for y1 in y for x1 in x]

    def open_csvfile(self, filename):
        """ Baixa a tranforma o arquivo com tabela do sudoku em uma lista. 
        Parametros:
            filename: Arquivo a ser inserido
        Retorno:
            list: Lista com todos os campos preenchidos e 0 caso None
        """
        with open(filename, 'r') as csv_file:
            value_list = []
            r = csv.reader(csv_file)
            value_list = [(row[col] if row[col] != "" else 0) for row in r for col in range(9)]
            return value_list

if __name__== "__main__":
    x = knowledge()
    x.head()