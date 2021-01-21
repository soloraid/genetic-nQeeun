import random
import heapq


class Chromosome:
    Genes = None
    cost = None

    def __init__(self, genes, cost):
        self.Genes = genes
        self.cost = cost

    def __lt__(self, other):
        return self.cost > other.cost


def _generate_parent(length, gene_set, get_cost):
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sampleSize))

    cost = get_cost(genes)
    return Chromosome(genes, cost)


def _mutate(parent, gene_set, get_cost):
    index = random.randrange(0, len(parent.Genes))
    childGenes = parent.Genes[:]
    newGene, alternate = random.sample(gene_set, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene

    cost = get_cost(childGenes)
    return Chromosome(childGenes, cost)


def reproduce(get_cost, parent1, parent2):
    cross_over = random.randrange(0, len(parent1.Genes), 2)
    list1 = list(parent1.Genes[:cross_over])
    list2 = list(parent2.Genes[cross_over:])
    list1.extend(list2)
    cost = get_cost(list1)
    return Chromosome(list1, cost)


def get_improvement(get_cost, new_child, generate_parent, mutate_prob, cross_prob, samples):
    global reproduce_child
    population_list = generate_parent(samples)
    population = []
    for parent in population_list:
        heapq.heappush(population, parent)
    new_population = []
    yield population
    while True:
        length = len(population)

        for index in range(0, length, 2):
            if random.random() <= cross_prob and index < length - 1:
                parent1 = heapq.heappop(population)
                parent2 = heapq.heappop(population)
                heapq.heappush(new_population, parent1)
                heapq.heappush(new_population, parent2)
                if random.random() <= mutate_prob:
                    reproduce_child = reproduce(get_cost, parent1, parent2)
                    if random.random() <= mutate_prob:
                        reproduce_child = new_child(reproduce_child)
                        if parent1.cost > reproduce_child.cost and parent2.cost > reproduce_child.cost:
                            continue
                        if not parent1.cost > reproduce_child.cost and parent2.cost > reproduce_child.cost:
                            heapq.heappush(new_population, reproduce_child)
                            continue
                        heapq.heappush(new_population, reproduce_child)
            else:
                parent1 = heapq.heappop(population)
                heapq.heappush(new_population, parent1)

        yield new_population
        population = new_population


def get_best(get_cost, target_len, optimal_cost, cross_prob, samples, mutate_prob, gene_set, display):
    random.seed()

    def fn_mutate(parent):
        return _mutate(parent, gene_set, get_cost)

    def fn_generate_parent(number_samples):
        population = list()
        while number_samples != -1:
            population.append(_generate_parent(target_len, gene_set, get_cost))
            number_samples = number_samples - 1
        return population

    for improvement in get_improvement(get_cost, fn_mutate, fn_generate_parent, mutate_prob, cross_prob, samples):

        chromosome = heapq.heappop(improvement)
        display(chromosome)
        if not optimal_cost > chromosome.cost:
            print('chromosomes: {0}\n'.format(len(improvement)))
            return chromosome
        if len(improvement) > 2000:
            print('chromosomes: {0}\n'.format(len(improvement)))
            return chromosome
        heapq.heappush(improvement, chromosome)
