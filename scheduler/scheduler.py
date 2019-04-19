import numpy
import itertools
import population
import time
import random
import math
import csv

SOL1 = [1,1,1,1,1,1,1,1,1,1,1,1]
SOL2 = [1,1,1,2,2,2,3,3,3,4,4,1]
SOL3 = [1,1,4,2,2,2,3,3,3,4,4,1]
SOL4 = [1,2,3,4,1,2,3,4,1,2,3,4]
POP_INI = [SOL1, SOL2, SOL3, SOL4]


class Scheduler:
    def __init__(self, filename):
        self.num_slots = 0
        self.num_courses = 0
        self.students_per_course = []
        self.incompatibilities = []

        self.read_input(filename)
        self.population = population.Population(self.num_courses, math.ceil(math.log(self.num_slots, 2)), POP_INI)
        self.calculate_incompatibilities()
        self.genetic_algorithm(POP_INI, 0.1)

    def read_input(self, filename):
        file_path = 'files/' + filename
        cnt = 1
        with open(file_path) as fp:
            line = fp.readline().strip()
            while line:
                line = line.split(" ")
                if cnt == 1:
                    self.num_slots = int(line[0])
                    self.num_courses = int(line[1])
                else:
                    course = list(map(lambda x: int(x)-1, line))
                    self.students_per_course.append(course)

                cnt += 1
                line = fp.readline().strip()

    def print_program(self):
        print("SLOTS: " + self.num_slots)
        print("COURSES: " + self.num_courses)
        i = 1
        for student in self.students_per_course:
            print("Student " + str(i) + ": ", end='')
            for course in student:
                print(course + " ", end='')

            print('')
            i += 1

    def calculate_incompatibilities(self):
        for i in range(self.num_courses):
            list_inc = []
            list1 = self.students_per_course[i]
            for j in range(i + 1, self.num_courses):
                list2 = self.students_per_course[j]
                list_inc.append(len(list(set(list1).intersection(list2))))
            self.incompatibilities.append(list_inc)
        #self.print_incompatibilites()


    def print_incompatibilites(self):
        for line in self.incompatibilities:
            for inc in line:
                print(inc, end=" ")
            print('')

    def fitness(self, individual):
        courses_per_slot = list()

        for i in range(self.num_slots):
            courses_per_slot.append(list())

        #courses per slot
        for i in range(self.num_courses):
            slot = individual.get_feature(i)
            if slot >= self.num_slots:
                return 0
            courses_per_slot[slot].append(i)

        total_incs = 0

        for slot in courses_per_slot:
            combinations = list(set(list(itertools.combinations(slot, 2))))

            slot_incs = 0
            for comb in combinations:
                min_val = min(comb[0], comb[1])
                max_val = max(comb[0], comb[1])
                slot_incs += self.incompatibilities[min_val][max_val-min_val-1]
            total_incs += slot_incs

        #print(total_incs)
        return 1/(total_incs+1)

    def max_fitness(self, population):
        max_fit = -1
        ind = None
        for individual in population.individuals:
            fitness = self.fitness(individual)
            if fitness > max_fit:
                max_fit = fitness
                ind = individual

        return ind, max_fit

    def get_parents(self, population):
        fitnesses = []
        aux = population.individuals

        for i in range(population.size):
            fitnesses.append(self.fitness(population.individuals[i]))


        parents = []
        while not (len(parents)*2 >= population.size):
            idx = fitnesses.index(max(fitnesses))
            parents.append(population.individuals[idx])
            del fitnesses[idx]
            del aux[idx]

        return parents


    def genetic_algorithm(self, ini_pop, mut_prob):
        start_time = time.time()

        # with open('results'+str(mut_prob)+".csv", 'w') as csvfile:
        #     filewriter = csv.writer(csvfile)


        pop = population.Population(self.num_courses, math.ceil(math.log(self.num_slots)), ini_pop)
        num_generations = 0
        max_ind = None

        while True:
            new_pop = population.Population(self.num_courses, math.ceil(math.log(self.num_slots)), [])
            new_pop.set_individuals(self.get_parents(pop))
            #new_pop.print()
            new_pop.crossover_and_mutate(mut_prob)
            pop = new_pop

            max_ind, fitness = self.max_fitness(pop)
            num_generations += 1
                #filewriter.writerow([str(num_generations), fitness])
            if num_generations > 4000:
                break

        #print("FITNESS", fitness)
        #print("--- %s seconds ---" % (time.time() - start_time))

        return fitness

scheduler = Scheduler("courses.txt")
