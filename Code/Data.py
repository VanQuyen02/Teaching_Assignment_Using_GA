from Course import Course
from Instructor import Instructor
import numpy as np
import pandas as pd
import os
class Data:
    def __init__(self):
        # Number of subjects taught in university
        self.Ns = None
        # Number of classes that need to be assigned to instructor
        self.Nc = None
        # Number of time slot
        self.Nt = None
        # Number of instructor
        self.Ng = None
        # Matrix S represents class C study subject S (1: True, 0: False)
        self.S = None
        # Matrix T represents class C is taught during time slot T (1: True, 0: False)
        self.T = None
        # Matrix A indicates level of preference of instructor G for subject S (level: 0-10)
        self.A = None
        # Matrix E indicates level of preference of instructor G for class C (level: 0-10)
        self.E = None # (self.Ng, self.Nc)
        # Matrix B indicates level of teaching quality of instructor G for subject S (level: 0-10)
        self.B = None
        # Matrix F indicates level of teaching quality of instructor G for class C (level: 0-10)
        self.F = None # (self.Ng, self.Nc)
        # Matrix C indicates level of preferences of instructor G for time slot T (level: 0-10)
        self.C = None
        # Matrix H indicates level of preferences of time slot T of instructor G for class C (level: 0-10)
        self.H = None #(self.Ng,self.Nc)
        # Vector K represent number of classes that instructor G want to teach (number: 0-10)
        self.K = None
        # Vector MinC indicates minimum number of classes that instructor G need to be assigned
        self.minC = None
        # Vector MaxC indicates maximum number of classes that instructor G need to be assigned
        self.maxC = None
        # Instructor
        self.instructors = None
        # Course
        self.courses = None

    def load_data(self):
        dir = 'D:/Course_FPT/Term_9/Reiforcement Learning/GA/TAS/data'
        subjects = pd.read_excel(os.path.join(dir, 'data_Sub.xlsx'))
        instructors = pd.read_excel(os.path.join(dir, 'data_T.xlsx'))
        courses = pd.read_excel(os.path.join(dir, 'sp22_to_import.xlsx'))
        instructor_time_slot_preference = pd.read_excel(os.path.join(dir, 'data_FSlot_T.xlsx'))
        instructor_time_slot_preference.drop(instructor_time_slot_preference.columns[0], axis=1, inplace=True)
        instructor_subject_preference = pd.read_excel(os.path.join(dir, 'data_FSlot_S.xlsx')) #, sheet_name=None)['Sheet2']
        instructor_subject_preference.drop(instructor_subject_preference.columns[0], axis=1, inplace=True)

        teaching_quantity = pd.read_excel(os.path.join(dir, 'data_Rating.xlsx'))
        teaching_quantity.drop(teaching_quantity.columns[0], axis=1, inplace=True)

        self.Ns = subjects.shape[0]
        self.Nc = courses.shape[0]
        self.Nt=  instructor_time_slot_preference.shape[1]
        self.Ng = instructors.shape[0]

        self.S = np.zeros((self.Nc, self.Ns))
        self.T = np.zeros((self.Nc,self.Nt))
        self.A = np.zeros((self.Ng, self.Ns))
        self.B = np.zeros((self.Ng, self.Ns))
        self.C = np.zeros((self.Ng, self.Nt))
        self.K = np.zeros((self.Ng,1))
        self.minC = np.zeros((self.Ng,1))
        self.maxC = np.zeros((self.Ng,1))
        self.instructors = [None]*self.Ng
        self.courses = [None]*self.Nc

       
        for i in range(1, self.Ng):
            id = i-1
            name = instructors['name'][i]
            salary_level = float(instructors['salary_level'][i])
            min_class = int(instructors['min_class'][i])
            self.minC[i-1][0] = min_class
            max_class = int(instructors['max_class'][i])
            self.maxC[i-1][0] = max_class
            ideal_class = int(instructors['ideal_class'][i])
            self.K[i-1][0] = ideal_class
            self.instructors[i-1]= Instructor(id, name, salary_level, min_class, max_class, ideal_class)
                
        for i, k in enumerate(instructor_time_slot_preference.keys()):
            for j in range(self.Ng):
                self.C[j, i] = int(instructor_time_slot_preference[k][j])

        
        for i in range(self.Ng):
            for j in range(self.Ns):
                self.B[i,j] = int(teaching_quantity[j][i])
        
        for i in range(self.Ng):
            for j in range(self.Ns):
                self.A[i,j] = int(instructor_subject_preference[j][i])
         
        for i in range (0, self.Nc):
            courseId = int(courses['CourseId'][i])
            className = courses['Class'][i]
            subjectName = courses['Subject'][i]
            subjectId = int(courses['SubjectId'][i])
            slotId = int(courses['SlotId'][i])
            room = courses['Room'][i]
            self.S[courseId][subjectId]=1
            self.T[courseId][slotId] = 1
            self.courses[i-1]= Course(courseId, className, subjectName, subjectId, slotId, room)

        self.E = self.A @ self.S.T
        self.F = self.B @ self.S.T
        self.H = self.C @ self.T.T


