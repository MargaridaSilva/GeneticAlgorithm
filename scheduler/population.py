from bitarray import *
import random
import struct
get_bin = lambda x, n: format(x, 'b').zfill(n)

class Individual:

    def __init__(self, num_features, feature_size, list):
        self.num_features = num_features
        self.feature_size = feature_size
        if len(list) > 0:
            bit_string = ""
            for elem in list:
                bit_string += get_bin(elem -1, feature_size)

            self.content = bitarray(bit_string)
        else:
            self.content = bitarray(self.feature_size*self.num_features)
            self.content.fill()

    def get_feature(self, idx):
        b = self.content[idx*self.feature_size:(idx+1)*self.feature_size]
        return int(b.to01(), 2)

    def mutate(self, mut_prob):
        if random.random() > mut_prob:
            for i in range(self.num_features*self.feature_size):
                if random.random() > mut_prob:
                    self.content[i] = not self.content[i]
        return self

    def print(self):
        for i in range(self.num_features):
            print(self.get_feature(i)+1, end ='')
        print('')

    def one_point_crossover(self, other):
        point = random.randint(1, self.num_features * self.feature_size - 1)
        child1 = Individual(self.num_features, self.feature_size, [])
        child2 = Individual(self.num_features, self.feature_size, [])
        child1.content[0:point-1] = self.content[0:point]
        child2.content[0:point - 1] = other.content[0:point]
        child2.content[point:self.num_features * self.feature_size - 1] = other.content[point:self.num_features * self.feature_size - 1]
        child1.content[point:self.num_features * self.feature_size - 1] = self.content[point:self.num_features * self.feature_size - 1]
        return child1, child2


class Population:
    def __init__(self, num_features, feature_size, individuals):
        self.individuals = []
        self.size = len(individuals)
        self.num_features = num_features
        self.feature_size = feature_size
        for individual in individuals:
            self.individuals.append(Individual(num_features, feature_size, individual))



    def set_individuals(self, individuals):
        self.individuals = individuals
        self.size = len(individuals)

    def add_individual(self, individual):
        self.individuals.append(individual)
        self.size +=1

    def print(self):
        for individual in self.individuals:
            individual.print()

    def get_random(self):
        n = random.randint(0, self.size-1)
        return self.individuals[n]

    def crossover_and_mutate(self, mut_prob):
        for i in range(0, self.size, 2):
            ind1 = self.individuals[i]
            ind2 = self.individuals[i+1]
            child1, child2 = ind1.one_point_crossover(ind2)
            child1.mutate(mut_prob)
            child2.mutate(mut_prob)
            self.add_individual(child1)
            self.add_individual(child2)

        self.size = len(self.individuals)

    def mutate(self):
        idx = self.size/2-1

        for i in range(idx, self.size):
            self.individuals.mutate()
