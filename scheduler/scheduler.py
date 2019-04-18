import numpy
import itertools
from . import population
import random

SOL1 = [1,1,1,1,1,1,1,1,1,1,1,1]
SOL2 = [1,1,1,2,2,2,3,3,3,4,4,1]
SOL3 = [1,1,4,2,2,2,3,3,3,4,4,1]
SOL4 = [1,2,3,4,1,2,3,4,1,2,3,4]


class Scheduler:
    def __init__(self, filename):
        self.num_slots = 0
        self.num_courses = 0
        self.students_per_course = []
        self.incompatibilities = []

        self.read_input(filename)
        self.calculate_incompatibilities()

        self.genetic_algorithm(SOL1)

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
                    self.students_per_course.append(list(map(int, line)))
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
        print(self.students_per_course)
        for i in range(self.num_courses):
            list_inc = []
            list1 = self.students_per_course[i]
            for j in range(self.num_courses):
                list2 = self.students_per_course[j]
                list_inc.append(len(list(set(list1).intersection(list2))))
            self.incompatibilities.append(list_inc)
        self.print_incompatibilites()

    def print_incompatibilites(self):
        for line in self.incompatibilities:
            for inc in line:
                print(inc, end=" ")
            print('')

    def fitness(self, solution):
        slots = list()
        for i in range(self.num_slots):
            slots.append(list())

        for i in range(len(solution)):
            slots[solution[i]-1].append(i)

        total_incs = 0

        for slot in slots:
            combinations = list(set(list(itertools.combinations(slot, 2))))
            slot_incs = 0
            for comb in combinations:
                slot_incs += self.incompatibilities[comb[0]][comb[1]]
            total_incs += slot_incs
        print(total_incs)

    def genetic_algorithm(self, ini_pop):
        new_pop = population.Population()
        for i in range(self.num_courses):
            # to do afterwards
            ind_1 = population.Individual(1)
            ind_2 = population.Individual(2)
            child = ind_1.reproduce(ind_2)
            if random.random(0, 1) < 0.1:
                child.mutate()
            new_pop.add_individual(child)

        while True


scheduler = Scheduler("courses.txt")

