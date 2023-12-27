import numpy as np

class Schedule:
    def __init__(self):
        pass
    # 3. An instructor cannot be assigned to teach different classes in the same time slot
    def checkConstraint3_before_assign(self, data, timetable_of_instructors, course, instructor):
        slot_Id = data.courses[course].slotId
        return timetable_of_instructors[instructor, slot_Id] == 0
    
    def checkConstraint3_after_assign(self, data, timetable_of_instructors, course, instructor):
        slot_Id = data.courses[course].slotId
        return timetable_of_instructors[instructor, slot_Id] == 1

    # 4. Do not assign instructors to teach the subjects they have absolutely no interest in teaching
    def checkConstraint4(self, data, course, instructor):
        return data.E[instructor, course] != 0

    # 5. Do not assign an instructor to teach the subjects they cannot ensure the quantity
    def checkConstraint5(self, data, course, instructor):
        return data.F[instructor, course] != 0

    # 6. Do not assign an instructor to teach in time slots they cannot teach
    def checkConstraint6(self, data, course, instructor):
        return data.H[instructor, course] != 0

    #7. Do not assign an instructor to teach fewer classes than the minimum number they are required to teach
    def checkConstraint7_before_assign(self, data, total_courses_of_instructors, instructor):
        total_courses_of_instructors[instructor] += 1
        total_course_need = 0
        total_assigned_course = 0

        for i in range(data.Ng):
            total_course_need += max(0, data.minC[i,0] - total_courses_of_instructors[i])
            total_assigned_course += total_courses_of_instructors[i]

        remain_course = data.Nc - total_assigned_course
        total_courses_of_instructors[instructor] -= 1
        result = total_course_need <= remain_course
        return result
    
    def checkConstraint7_after_assign(self, data, total_courses_of_instructors, instructor):
        return total_courses_of_instructors[instructor] >= data.minC[instructor][0]
    # 8. Do not assign an instructor to teach more classes than the maximum number they are allowed to teach
    def checkConstraint8(self, data, total_courses_of_instructors, instructor):
        return total_courses_of_instructors[instructor] < data.maxC[instructor][0]

    def check_all_constraint_before_assign(self, data, total_courses_of_instructors, timetable_of_instructors, course, instructor):
        return (self.checkConstraint3_before_assign(data, timetable_of_instructors, course, instructor) and
                self.checkConstraint4(data, course, instructor) and
                self.checkConstraint5(data, course, instructor) and
                self.checkConstraint6(data, course, instructor) and
                self.checkConstraint7_before_assign(data, total_courses_of_instructors, instructor) and
                self.checkConstraint8(data, total_courses_of_instructors, instructor))
    def check_all_constraint_after_assign(self, data, total_courses_of_instructors, timetable_of_instructors, course, instructor):
        return (self.checkConstraint3_after_assign(data, timetable_of_instructors, course, instructor) and
                self.checkConstraint4(data, course, instructor) and
                self.checkConstraint5(data, course, instructor) and
                self.checkConstraint6(data, course, instructor) and
                self.checkConstraint7_after_assign(data, total_courses_of_instructors, instructor) and
                self.checkConstraint8(data, total_courses_of_instructors, instructor))

    def create_chromosome(self, data):
        chromosome = np.full(data.Nc, fill_value=-1, dtype=int)
        total_courses_of_instructors = np.zeros(data.Ng, dtype=int)
        timetable_of_instructors = np.zeros((data.Ng, data.Nt), dtype=int)

        for i in range(data.Nc):
            while True:
                random_instructor = np.random.randint(0, data.Ng)
                if self.check_all_constraint_before_assign(data, total_courses_of_instructors, timetable_of_instructors, i,
                                             random_instructor):
                    chromosome[i] = random_instructor
                    total_courses_of_instructors[random_instructor] += 1
                    slotId = data.courses[i].slotId
                    timetable_of_instructors[random_instructor, slotId] = 1
                    break
        return chromosome

    def calPayoffP0(self,data, D):
        # D shape(Nc,1) D[i] là 1 instructor
        payoff_p0 = 0
        for i in range(data.Nc):
            payoff_p0 += data.F[D[i]][i]
        return payoff_p0
    
    def calPayoffPi(self,data, D):
        w1 = 1.0 / 3.0
        w2 = 1.0 / 3.0
        w3 = 1.0 / 3.0
        payoff_pi = np.zeros(data.Ng,dtype=float)
        total_courses_of_instructors = np.zeros(data.Ng,dtype=int)
        timetable_of_instructors = np.zeros((data.Ng, data.Nt),dtype=int)
        for i in range(data.Nc):
            instructor = D[i]
            payoff_pi[instructor] += w1 * data.E[instructor][i] + w2 * data.H[instructor][i]
            total_courses_of_instructors[instructor] += 1
            slotId = data.courses[i].slotId
            timetable_of_instructors[instructor, slotId] = 1

        for i in range(data.Ng):
            payoff_pi[i] += w3 * (10 - abs(data.K[i] - total_courses_of_instructors[i]))

        return timetable_of_instructors, total_courses_of_instructors, payoff_pi
    
    def getFitness(self, data, chromosome):
        w4 = 0.5
        w5 = 0.5
        P0_value = self.calPayoffP0(data, chromosome)
        timetable_of_instructors, total_courses_of_instructors, Pi_value = self.calPayoffPi(data, chromosome)
        Pi_value = sum(i for i in Pi_value)
        fitness_value = w4*P0_value+w5*Pi_value
        flag = True
        print(total_courses_of_instructors.shape)
        print(data.maxC.shape)
        for i in range(len(chromosome)):
            print(total_courses_of_instructors[chromosome[i]] < data.maxC[chromosome[i]][0])
            # if self.check_all_constraint_after_assign(data, total_courses_of_instructors, timetable_of_instructors, i,
            #                                  chromosome[i])== False:
            #     print(self.checkConstraint3_after_assign(data, timetable_of_instructors, i, chromosome[i]),\
            #     self.checkConstraint4(data, i, chromosome[i]),\
            #     self.checkConstraint5(data, i, chromosome[i]),\
            #     self.checkConstraint6(data, i, chromosome[i]),\
            #     self.checkConstraint7_after_assign(data, total_courses_of_instructors, chromosome[i]),\
            #     self.checkConstraint8(data, total_courses_of_instructors, chromosome[i]))
            flag= False
        print(flag)
        if(flag==False):
            fitness_value = fitness_value/1000
        return fitness_value
    
    