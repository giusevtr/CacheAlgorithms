import numpy as np
from lib.aux import *
class Markov :

    def __init__(self, adj_mat) :
        self.A = adj_mat

    def random_walk_distribution(self, start_page) :
        A = self.A[:,:]
        n = len(A)

        # Starting configuration
        R = np.zeros(n)
        R[start_page] = 1

        M = matrix_pow(A, n)
        R = np.matmul(M,R)

        return R
