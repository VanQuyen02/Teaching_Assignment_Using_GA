from Schedule import Schedule
from Data import Data


if __name__ == "__main__":
    data = Data()
    data.load_data()
    solution = Schedule()
    chromosome = solution.create_chromosome(data)
    fitness_value = solution.getFitness(data,chromosome)
    print(chromosome)
    print(fitness_value)