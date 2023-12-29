from Schedule import Schedule
import random

S = Schedule()
class GA_Algorithm:
    def __init__(self, data, numberChromosome, numberIteration, numberCrossOver, numberMutation):
        self.data = data
        self.numberChromosome = numberChromosome
        self.numberIteration = numberIteration
        self.numberCrossover = numberCrossOver
        self.numberMutation = numberMutation

    def run_GA_Algorithm(self):
        bestSchedule = []
        # initialize population with pop_size = self.numberChromosome
        currentPopulation = self.initializePopulation()
        # Choose bestSchedule from iteration
        bestSchedule = self.iterateGeneration(currentPopulation, bestSchedule)
        return bestSchedule

    def iterateGeneration(self, currentPopulation, bestSchedule):
        # iteration
        for i in range(self.numberIteration):
            # Sort by decreasing of fitness
            currentPopulation = self.sortPopulation(currentPopulation)
            # Add best schedule to the list
            bestSchedule.append(currentPopulation[0])
            # Selection phase: Choose top k and not top k best elite chromosome from population
            k = 30
            top_k_elite_p1, not_top_k_elite_p1 = self.selection(currentPopulation, k)
            # Crossover phase: Generate another population with the same initial pop_size from not top k best elite chromosome from population

            currentPopulation = top_k_elite_p1 + self.crossOver(not_top_k_elite_p1, self.numberCrossover)
            # Mutation phase: Generate source for selection phase with n_mutations
            currentPopulation = self.mutation(currentPopulation, self.numberMutation)
            # Sort by decreasing of fitness
            currentPopulation = self.sortPopulation(currentPopulation)
            # Selection phase: Choose 300- k best elite chromosome from P'
            top_k_elite_p3, _ = self.selection(currentPopulation, self.numberChromosome - k)
            # Set current population
            currentPopulation = top_k_elite_p1 + top_k_elite_p3

        bestSchedule = self.sortPopulation(currentPopulation)[0]
        return bestSchedule

    def initializePopulation(self):
        numberChromosome = self.numberChromosome
        population = []
        for i in range(numberChromosome):
            chromosome = S.create_chromosome(self.data)
            population.append(chromosome)
        return population

    def sortPopulation(self, currentPopulation):
        sortedPopulation = []
        population_with_fitness = []
        for chromosome in currentPopulation:
            fitness_value = S.calculateFitness(self.data, chromosome)
            population_with_fitness.append([chromosome, fitness_value])
        population_with_fitness.sort(population_with_fitness, key=lambda x: x[1], reverse=True)
        for item in population_with_fitness:
            chromosome = item[0]
            sortedPopulation.append(chromosome)
        return sortedPopulation

    def selection(self, sortedPopulation, k):
        top_k_elite = sortedPopulation[:k]
        not_top_k_elite = sortedPopulation[k:]
        return top_k_elite, not_top_k_elite

    def crossOver(self, population, populationSize):
        newPopulation = [None] * populationSize
        for i in range(populationSize):
            while True:
                mother_index = random.randint(0, len(population))
                father_index = random.randint(0, len(population))
                if mother_index != father_index:
                    mother = population[mother_index]
                    father = population[father_index]
                    child = father[:(len(father) // 2)] + mother[(len(mother) // 2):]
                    newPopulation[i] = child
                    break

    def mutation(self, population, numberMutation):
        populationSize = len(population)
        j = 0
        for i in range(populationSize):
            chromosome = population[i]
            for j in range(numberMutation):
                while True:
                    course1 = random.randint(0, len(chromosome))
                    course2 = random.randint(0, len(chromosome))
                    instructor1 = chromosome[course1]
                    instructor2 = chromosome[course2]
                    if instructor1 != instructor2:
                        temp = chromosome[course1]
                        chromosome[course1] = chromosome[course2]
                        chromosome[course2] = temp
                        break
        return population
