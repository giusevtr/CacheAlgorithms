from scipy.sparse import csc_matrix
import numpy as np

class Pagerank:


    def compute_local(self, A, E,maxerr = 0.1, maxiter = 100) :

        R = np.copy(E)
        delta = 1e9
        while delta > maxerr and maxiter > 0:

            Rt = np.matmul(A,R)
            d = np.sum(np.abs(R)) - np.sum(np.abs(Rt))
            Rt = Rt + d * E
            delta = np.sum(np.abs(Rt - R))

            R = np.copy(Rt)

            # print('delta = %lf' % delta)
            maxiter -=1

        return R


    def compute(self,G, s = .85, maxerr = .0001):
        """
        Computes the pagerank for each of the n states
        Parameters
        ----------
        G: matrix representing state transitions
           Gij is a binary value representing a transition from state i to j.
        s: probability of following a transition. 1-s probability of teleporting
           to another state.
        maxerr: if the sum of pageranks between iterations is bellow this we will
                have converged.
        """
        n = G.shape[0]
        print("debug!!!!!!!!!!!!!!!")
        # transform G into markov matrix A
        A = csc_matrix(G,dtype=np.float)
        rsums = np.array(A.sum(1))[:,0]
        ri, ci = A.nonzero()
        A.data /= rsums[ri]

        # bool array of sink states
        sink = rsums == 0

        # Compute pagerank r until we converge
        ro, r = np.zeros(n), np.ones(n)
        while np.sum(np.abs(r-ro)) > maxerr:
            ro = r.copy()
            # calculate each pagerank at a time
            for i in range(0,n):
                # inlinks of state i
                Ai = np.array(A[:,i].todense())[:,0]
                # account for sink states
                Di = sink / float(n)
                # account for teleportation to state i
                # Ei = np.ones(n) / float(n)
                Ei = teleport_vector[:]

                r[i] = ro.dot( Ai*s + Di*s + Ei*(1-s) )

        # return normalized pagerank
        return r/float(sum(r))
