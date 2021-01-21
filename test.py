import unittest
import datetime
import genetic


class Results:
    chromosomes = set()
    sizes = set()
    start_times = set()

    def __init__(self, chromosome, size, start_time):
        self.chromosomes.add(chromosome)
        self.sizes.add(size)
        self.start_times.add(start_time)


class NQueensTests(unittest.TestCase):
    # board_results = set()

    def test_1(self, size=8, samples=10, mutate_prob=0.2, cross_prob=0.8):
        gene_set = [i for i in range(size)]
        self.compute(size, gene_set, samples, mutate_prob, cross_prob)

    def test_2(self, size=8, samples=100, mutate_prob=0.3, cross_prob=0.6):
        gene_set = [i for i in range(size)]
        self.compute(size, gene_set, samples, mutate_prob, cross_prob)

    def test_3(self, size=20, samples=100, mutate_prob=0.4, cross_prob=0.8):
        gene_set = [i for i in range(size)]
        self.compute(size, gene_set, samples, mutate_prob, cross_prob)

    def test_4(self, size=20, samples=1000, mutate_prob=0.3, cross_prob=0.7):
        gene_set = [i for i in range(size)]
        self.compute(size, gene_set, samples, mutate_prob, cross_prob)

    def test_5(self, size=50, samples=1000, mutate_prob=0.3, cross_prob=0.7):
        gene_set = [i for i in range(size)]
        self.compute(size, gene_set, samples, mutate_prob, cross_prob)

    def compute(self, size, gene_set, samples, mutate_prob, cross_prob):
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            display(candidate, start_time, size)
            print("size: {0}\nInitial_samples: {1}\n".format(size, samples))

        def fn_get_cost(genes):
            return get_cost(genes, size)

        optimal_cost = Cost(0)
        best = genetic.get_best(fn_get_cost, 2 * size, optimal_cost, cross_prob,
                                samples, mutate_prob, gene_set, fn_display)

        self.assertTrue(not optimal_cost > best.cost)
        # self.board_results.add(Results(best, size, start_time))
        print('#############END ITERATION#################')


class Board:

    def __init__(self, genes, size):
        board = [['.'] * size for _ in range(size)]
        for index in range(0, len(genes), 2):
            row = genes[index]
            column = genes[index + 1]
            board[column][row] = 'Q'
        self._board = board

    def get(self, row, column):
        return self._board[column][row]

    def printing(self):
        for i in reversed(range(0, len(self._board))):
            print(' '.join(self._board[i]))


class Cost:
    total = None

    def __init__(self, total):
        self.total = total

    def __gt__(self, other):
        return self.total < other.total

    def __str__(self):
        return '{0}'.format(self.total)


def display(candidate, start_time, size):
    timeD = datetime.datetime.now() - start_time

    if str(candidate.cost) == '0':
        board = Board(candidate.Genes, size)
        board.printing()
    print("chromosome_goal: {0}\ncost: {1}\ntime: {2}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.cost,
        str(timeD)))


def get_cost(genes, size):
    board = Board(genes, size)
    rowQs = set()
    columnQs = set()
    primaryDiaQs = set()
    secondaryDiaQs = set()
    for row in range(size):
        for col in range(size):
            if board.get(row, col) == 'Q':
                rowQs.add(row)
                columnQs.add(col)
                primaryDiaQs.add(row + col)
                secondaryDiaQs.add(size - 1 - row + col)

    total = 4 * size - len(rowQs) - len(columnQs) - len(primaryDiaQs) - len(secondaryDiaQs)

    return Cost(total)


def running_single_test(testcase):
    switcher = {
        1: 'test_1',
        2: 'test_2',
        3: 'test_3',
        4: 'test_4',
        5: 'test_5',
    }
    return switcher.get(testcase, 'Wrong choice')


if __name__ == "__main__":
    while True:
        single_test = unittest.TestSuite()
        print('{0}:\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format('Menu', '1.size=8 & init = 10',
                                                            '2.size=8 & init = 100',
                                                            '3.size=20 & init = 100',
                                                            '4.size=20 & init = 1000',
                                                            '5.size=50 & init = 1000',
                                                            '6.exit'))
        test_case = int(input('\n\nEnter your choice: '))
        if test_case == 6:
            break
        test_name = running_single_test(test_case)
        if test_name != 'Wrong choice':
            single_test.addTest(NQueensTests(test_name))
            unittest.TextTestRunner().run(single_test)
        else:
            print(test_name)
