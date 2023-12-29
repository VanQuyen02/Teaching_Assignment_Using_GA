from Data import Data
from GA_Algorithm import GA_Algorithm
from Schedule import Schedule
if __name__ == "__main__":
    s = Schedule()
    data = Data()
    data.load_data()
    numberChromosome = 300
    numberIteration = 300
    numberMutation = 5
    gaRun = GA_Algorithm(data, numberChromosome, numberIteration, numberMutation) 
    numberRunTime = 1      
    for i in range(numberRunTime):
        bestSchedule = gaRun.run_GA_Algorithm()
        print(bestSchedule, s.getFitness(data, bestSchedule))
    