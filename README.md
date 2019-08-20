# sudoku_m
Algoritmo para resolução do jogo sudoku

Versão 2.0: Este algoritmo está apto a resolver qualquer nível do puzzle
- Nos arquivos se encontra uma tabela conhecida como "World Hardest Sudoku" pela revista(?) The Telegraph, que é o exemplo mais insano que encontrei do jogo.
- Na primeira versão eu estive usando numpy para montar a tabela, porem após uma idéia genial que encontrei em um artigo chamado "Sudoku Solver by Peter Norvig"(link : https://medium.com/activating-robotic-minds/peter-norvigs-sudoku-solver-25779bb349ce), achei bem interessante usar um mapeamento estilo batalha naval.

* Certifique-se que a tabela a ser inserida está correta, pois tabela impossíveis não serão completadas.

File de Input:
    - Arquivo em CSV separado por virgulas(","), é bem chato para o posicionamento, porêm obriga a ter atenção na inserção dos valores. Além disso, o codigo printa a tabela antes das instancias começarem a atuarem nesta.

Introdução:
    - Para iniciar o programa, basta dar um "python knowledge.py" no prompt, ou somente iniciar o arquivo(método main já implementado)