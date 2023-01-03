# Суть моего решения состоит в том, чтобы, для определения списывания,
# рассмотреть изменения в общей структуре кода, а не изменения в названиях переменных или функицй.
# Ведь в ходе копирования именно их и меняет ленивый студент, стараясь избежать подозрений.
# Структуру кода при этом он меняет мало: удаляет или вставляет компоненты, меняет их местами.
# Поэтому в моем решении используется измененный алгоритм Левенштайна, позволяющий учесть перестановку
# соседей двух последовательностей (алг. Дамерау — Левенштейна).

# Конечный балл (score) выставляется по формуле:
# 1 - Расстояние/max(Длина первой последовательности, Длина второй последовательности)
# Конечно же вид формулы можно и усложнить, чтобы более баллы точно описывали присутстсвие копирования.
# При данном виде формулы, работы со score > 0.6 я бы подозревал в списывании.

import ast
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
args = parser.parse_args()


class Analyzer(ast.NodeVisitor):
    """Класс для анализа AST"""

    def __init__(self):
        self.statements_ = []

    def generic_visit(self, node):
        """Функция, рекурсивно посещающая узлы дерева, собирая их типы"""
        name = type(node).__name__

        if isinstance(node, (ast.stmt, ast.operator, ast.expr)) and not isinstance(node, ast.Expr):
            self.statements_.append(name)

        ast.NodeVisitor.generic_visit(self, node)

    def report(self):
        """Функция возвращающая результат прохода по дереву и отсева ненужных типов узлов"""
        return self.statements_


def damerau_levenshtein_distance(a1, a2):
    """
    Получает на вход две последовательности, возвращает расстояние Дамерау-Левенштайна между ними.
    Цена за делецию, вставку, замену и транспозицию одинакова и равна 1.
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    """

    d = {}
    len1 = len(a1)
    len2 = len(a2)

    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1

    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            if a1[i] == a2[j]:
                cost = 0
            else:
                cost = 1

            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )

            if i and j and a1[i] == a2[j - 1] and a1[i - 1] == a2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + 1)  # transposition

    return d[len1 - 1, len2 - 1]


def main():
    output_file = open(args.output_file, 'w')
    with open(args.input_file, 'r') as input_file:

        for line in input_file.read().splitlines():

            in_dir1, in_dir2 = line.split(' ')

            with open(in_dir1, 'r', encoding='utf-8') as source1, \
                    open(in_dir2, 'r', encoding='utf-8') as source2:
                # собираем данные с двух файлов
                tree1, tree2 = ast.parse(source1.read()), ast.parse(source2.read())

                analyzer = Analyzer()

                analyzer.visit(tree1)
                statements1_ = analyzer.report()

                analyzer.__init__()

                analyzer.visit(tree2)
                statements2_ = analyzer.report()
                # вычисляем расстояние и конечный балл
                lev_score = damerau_levenshtein_distance(statements1_, statements2_)

                max_len = max([len(statements1_), len(statements2_)])
                final_score = 1 - lev_score/max_len

                output_file.write(f'{round(final_score, 2)}\n')

    output_file.close()


if __name__ == "__main__":
    main()
