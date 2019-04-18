from bitarray import *
import random
get_bin = lambda x: format(x, 'b')

class Individual:
    def __init__(self, num_features, feature_size, list):
        self.num_features = num_features
        self.feature_size = feature_size
        self.content = bitarray(self.num_features*self.feature_size)
        for elem in list:
            binary_rep = get_bin(elem)
            #to do: representation?

    def get_feature(self, idx):
        return self.content[idx*self.feature_size]

    def mutate_one(self):
        n = random(0, self.num_features*self.feature_size)
        self.content[n] = not self.content[n]


class Population:
    def __init__(self, num_features, feature_size, individuals):
        self.individuals = []
        for individual in individuals:
            self.individuals.append(Individual(num_features, feature_size, individual))

