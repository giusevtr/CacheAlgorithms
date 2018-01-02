import random
import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import tensorflow as tf
import numpy as np
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ANN1(page_replacement_algorithm):

    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.disk = Disk(N)
        
        ###############################################
        learning_rate = 0.1
        
        self.X = tf.placeholder(dtype=tf.float32, shape=[None, 3*M], name="input")
        self.Y = tf.placeholder(dtype=tf.float32, shape=[None, 3*M], name="output")
        
#         R = tf.Variable(tf.random_uniform([M,1]))
#         F = tf.Variable(tf.random_uniform([M,1]))
#         Z = tf.constant(np.ones((M,M)) - np.eye(N, M))
        
        W = tf.Variable(tf.random_uniform([3*M, M]))
        
        
        cmat = np.zeros((3*M, M))
        cmat[0:M,:] = np.eye(M, M)
        cmat[M:2*M,:] = np.eye(M, M)
        cmat[2*M:3*M,:] = np.ones((M,M)) - np.eye(M, M)
        
        
        output_layer = tf.nn.softmax(tf.matmul(self.X, tf.matmul(W,cmat)))
        
        
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output_layer, self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
        
        
        self.evitpage = tf.argmin(output_layer + tf.ones(shape=[3*M]) - self.X)
        
        init = tf.initialize_all_variables()
        
        self.sess = tf.Session()
        self.sess.run(init)
        
        
         
    def get_N(self) :
        return self.N
    
    def getState(self):
        x = np.zeros(3*self.M)
        for i in self.disk :
            x[i] = 1
            x[self.M + i] = 1
            x[2*self.M + i] = 1
        return x
    
    def request(self,page) :
        page_fault = False
        if self.disk.inDisk(page) :
            self.disk.moveBack(page)
        else :
            #if len(self.T)  == self.N :
            if self.disk.size() == self.N :
                ## Remove LRU page
                X = self.getState()
                least_likely_page = self.sess.run(self.evitpage, feed_dict={self.X : X})
                
                
                self.disk.delete(least_likely_page)
            # Add page to the MRU position
            self.disk.add(page)
            page_fault = True

        return page_fault

    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.disk.get_data()]

    def get_list_labels(self) :
        return ['L']

if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print("Error: Must supply cache size.")
        print("usage: python3 [cache_size]")
        exit(1)

    n = int(sys.argv[1])
    print("cache size ", n)

    marking = LRU(n)
    page_fault_count = 0
    page_count = 0
    for line in sys.stdin:
        #print("request: ", line)
        if marking.request(line) :
            page_fault_count += 1
        page_count += 1


    print("page count = ", page_count)
    print("page faults = ", page_fault_count)
