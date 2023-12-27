from Schedule import Schedule
import random
class GA:
    def __init__(self,data, numberChromosome, numberIteration,numberMutation):
        self.data = data
        self.numberChromosome = numberChromosome
        self.numberIteration = numberIteration
        self.numberMutation = numberMutation

s = Schedule()
class GA_Algorithm:
    def __init__(self):
        pass
    def run_GA_Algorithm(self, ga):
        bestSchedule = []
        # initialize population with pop_size = ga.numberChromosome
        currentPopulation= self.initializePopulation(ga)
        # Choose bestSchedule from iteration
        bestSchedule = self.iterateGeneration(currentPopulation, bestSchedule, ga)
        return bestSchedule
    
    def iterateGeneration(self, currentPopulation, ga,bestSchedule):
        # iteration
        for i in range(ga.numberIteration):
            # Sort by decreasing of fitness
            currentPopulation = self.sortPopulation(currentPopulation, ga)
            # Add best schedule to the list
            bestSchedule.append(currentPopulation[0])
            # Selection phase: Choose top k and not top k best elite chromosome from population
            k = 30
            top_k_elite_p1, not_top_k_elite_p1 = self.selection(currentPopulation,k)
            # Crossover phase: Generate another population with same initial pop_size from not top k best elite chromosome from population
            populationSize = ga.numberChromosome
            currentPopulation = self.crossOver(not_top_k_elite_p1, populationSize)
            # Sort by decreasing of fitness
            currentPopulation = self.sortPopulation(currentPopulation, ga)
            # Selection phase: Choose top k and not top k best elite chromosome from population
            top_k_elite_p2, not_top_k_elite_p2 = self.selection(currentPopulation,k)
            # Mutation phase : Generate source for selection phase with n_mutations
            not_top_k_elite_p2 = self.mutation(not_top_k_elite_p2, ga.numberMutation)
            currentPopulation = top_k_elite_p2 + not_top_k_elite_p2
            # Sort by decreasing of fitness
            currentPopulation = self.sortPopulation(currentPopulation, ga)
            # Selection phase: Choose 300- k best elite chromosome from P'
            top_k_elite_p3,_ = self.selection(currentPopulation,ga.numberChromosome-k)
            # Set current population
            currentPopulation = top_k_elite_p1 + top_k_elite_p3
        
        bestSchedule = self.sortPopulation(currentPopulation, ga)[0]
        return bestSchedule

    def initializePopulation(self,ga):
        numberChromosome = ga.numberChromosome
        population = []
        for i in range(numberChromosome):
            chromosome = s.create_chromosome(ga.data)
            population.append(chromosome)
        return population

    def sortPopulation(self,currentPopulation,ga):
        sortedPopulation = []
        population_with_fitness =[]
        for chromosome in currentPopulation:
            fitness_value = s.calculateFitness(ga.data, chromosome)
            population_with_fitness.append([chromosome, fitness_value])
        population_with_fitness.sort(population_with_fitness, key=lambda x: x[1], reverse=True)
        for item in population_with_fitness:
            chromosome = item[0]
            sortedPopulation.append(chromosome)
        return sortedPopulation

    def selection(self, sortedPopulation,k):
        top_k_elite = sortedPopulation[:k]
        not_top_k_elite = sortedPopulation[k:]
        return top_k_elite, not_top_k_elite

    def crossOver(self, population, populationSize):
        newPopulation = [None]*populationSize
        for i in range(populationSize):
            while True:
                mother_index = random.randint(0,len(population))
                father_index = random.randint(0,len(population))
                if(mother_index!= father_index):
                    mother = population[mother_index]
                    father = population[father_index]
                    child = father[:(len(father)//2)]+mother[(len(mother)//2):]
                    newPopulation[i] = child
                    break


    def mutation(self, population, numberMutation):
        populationSize = len(population)
        j =0
        for i in range(len(populationSize)):
            chromosome = population[i]
            for j in range(numberMutation):
                while True:
                    course1 = random.randint(0, len(chromosome))
                    course2 = random.randint(0, len(chromosome))
                    instructor1 = chromosome[course1]
                    instructor2 = chromosome[course2]
                    if(instructor1 != instructor2):
                        temp = chromosome[course1]
                        chromosome[course1] = chromosome[course2]
                        chromosome[course2] = temp
                        break
        return population
