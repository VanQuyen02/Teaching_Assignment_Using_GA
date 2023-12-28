import random

class DistributedRandomNumberGenerator:
    def __init__(self):
        self.distribution = {}
        self.dist_sum = 0.0

    @staticmethod
    def get_random_number(min_val, max_val):
        return int((random.random() * (max_val - min_val)) + min_val)

    def get_dist_sum(self):
        return self.dist_sum

    def add_number(self, value, distribution):
        if value in self.distribution:
            self.dist_sum -= self.distribution[value]
        self.distribution[value] = distribution
        self.dist_sum += distribution

    def get_distributed_random_number(self):
        rand = random.random()
        ratio = 1.0 / self.dist_sum
        temp_dist = 0

        for i in self.distribution:
            temp_dist += self.distribution[i]
            if rand / ratio <= temp_dist:
                return i
        return 0