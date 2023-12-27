from Data import Data
from GA_Algorithm import GA, GA_Algorithm

if __name__ == "__main__":
    data = Data()
    data.load_data()
    numberChromosome = 500
    numberIteration = 10000
    numberMutation = 50

    ga = GA(data, numberChromosome, numberIteration, numberMutation)   
    gaRun = GA_Algorithm()
    
    numberRunTime = 4
        
    for i in range(numberRunTime):
        bestSchedule = gaRun.run_GA_Algorithm(ga)
        print(bestSchedule)
    