from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
from lib.CacheLinkedList import CacheLinkedList
import tensorflow as tf
import numpy as np
import Queue
import heapq
# import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class OLCR_RAND(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.CacheRecency = CacheLinkedList(N)

        self.freq = {}
        self.PQ = []
        
        self.Hist1 = CacheLinkedList(N)        
        self.Hist2 = CacheLinkedList(N)        
        
        ## Config variables
        self.epsilon = 0.90
        self.error_discount_rate = (0.005)**(1.0/N)
        
        ## 
        self.policy = 0
        self.evictionTime = {}
        self.policyUsed = {}
        self.pUsed = {}
        self.param = {}
        
        
        ## Accounting variables
        self.time = 0
        
        ###
        self.q = Queue.Queue()
        self.sum = 0
        self.NewPages = []
        
        
        self.c_hits = 0
        self.h_miss = 0
        
        self.learning = True
        
        
        self.X = tf.placeholder(dtype=tf.int32, shape=[None,2])
        self.P = tf.placeholder(dtype=tf.float32, shape=[None,1])
        
        self.R = tf.placeholder(dtype=tf.float32, shape=[None])
        self.F = tf.placeholder(dtype=tf.float32, shape=[None])
        
        self.W = tf.Variable(tf.random_uniform([2*self.N]))
        
        
        
#         self.predict = tf.sigmoid(tf.matmul(self.X, self.W))
#         self.predict = tf.sigmoid(tf.slice(self.W, self.X[0,0],[1]) + tf.slice(self.W, self.X[0,1]+self.N,[1]))
        idx1 = tf.slice(self.X,[0,0],[-1,1])
        idx2 = tf.slice(self.X,[0,1],[-1,1])
        
        
        self.w1 = tf.slice(self.W, idx1[0] ,[1])
        self.w2 = tf.slice(self.W, idx2[0] ,[1])
        
        self.predict = tf.sigmoid(self.w1 + self.w2)
        
        
        
        self.cost = tf.reduce_sum(self.R * tf.log(self.predict) + self.F * tf.log(1 - self.predict))
        learning_rate = 0.1
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)
        
        
        ##################################
        self.X_holder = []
        self.P_holder = []
        self.R_holder = []
        self.F_holder = []
        self.train_batch_size = 5*self.N
        
        init = tf.global_variables_initializer()
        
        self.sess = tf.Session()
        self.sess.run(init)
        
        
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        return []
    
    ##############################################################
    ## There was a page hit to 'page'. Update the data structures
    ##############################################################
    def pageHitUpdate(self, page):
        assert page in self.CacheRecency and page in self.freq
        self.CacheRecency.moveBack(page)
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
    
    ##########################################
    ## Add a page to cache using policy 'poly'
    ##########################################
    def addToCache(self, page):
        self.CacheRecency.add(page)
        if page not in self.freq :
            self.freq[page] = 0
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
    
    def getHeapMin(self):
        
        if len(self.PQ) < self.N :
            print self.PQ
        
        assert len(self.PQ) >= self.N, 'PQ should be full %d' % len(self.PQ)
        while self.PQ[0][1] not in self.CacheRecency or self.freq[self.PQ[0][1]] != self.PQ[0][0] :
            heapq.heappop(self.PQ) 
        return self.PQ[0][1]
    
    ######################
    ## Get LFU or LFU page
    ## return page, poly
    ######################    
    def selectEvictPage(self, P):
        assert P >= 0 and P <= 1
        if np.random.rand() < P :
            return self.CacheRecency.getFront(), 0 
        else:
            return self.getHeapMin(), 1
    
    def evictPage(self, pg):
        assert pg in self.CacheRecency
        self.CacheRecency.delete(pg)
        
    
    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self):
        r = np.random.rand()
        if r < self.W[0] :
            return 0
        return 1
    
    def addToHistory(self, poly, cacheevict):
        histevict = None
        if (poly == 0) or (poly==-1 and np.random.rand() <0.5):
            if self.Hist1.size() == self.N :
                histevict = self.Hist1.getFront()
                assert histevict in self.Hist1
                self.Hist1.delete(histevict)
            self.Hist1.add(cacheevict)
        else:
            if self.Hist2.size() == self.N :
                histevict = self.Hist2.getFront()
                assert histevict in self.Hist2
                self.Hist2.delete(histevict)
            self.Hist2.add(cacheevict)
            
        if histevict is not None :
            del self.evictionTime[histevict]
            del self.policyUsed[histevict]
            del self.freq[histevict]
            del self.pUsed[histevict]
            del self.param[histevict]
            
            
            
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        
        
        ###########################
        ## Clean up
        ## In case PQ get too large
        ##########################
        if len(self.PQ) > 2*self.N:
            newpq = []
            for pg in self.CacheRecency :
                newpq.append((self.freq[pg],pg))
            heapq.heapify(newpq)
            self.PQ = newpq
            del newpq
        
        
        page_outcome = -1
        
        ##########################
        ## Process page request 
        ##########################
        if page in self.CacheRecency:
            page_fault = False
            self.pageHitUpdate(page)
            page_outcome = 1
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            
            if page in self.Hist1 or page in self.Hist2:
                page_outcome = 2
                if page in self.Hist1 :
                    self.Hist1.delete(page)
                else:
                    self.Hist2.delete(page)
                
            ####################
            ## Remove from Cache
            ####################
            if self.CacheRecency.size() == self.N:
                
                ################
                ## Choose Policy
                ################
                P = np.random.rand()
                cacheevict,poly = self.selectEvictPage(P)
                
                self.policyUsed[cacheevict] = poly
                self.evictionTime[cacheevict] = self.time
                self.pUsed[cacheevict] = P
                self.param[cacheevict] = [self.c_hits, self.h_miss]
                
                ###################
                ## Remove from Cache and Add to history
                ###################
                self.evictPage(cacheevict)
                self.addToHistory(poly, cacheevict)
                
            self.addToCache(page)
            
            page_fault = True

        self.q.put(page_outcome)
        
        if page_outcome == 1 :
            self.c_hits += 1 
        elif page_outcome == 2 :
            self.h_miss += 1
        
        if self.q.qsize() >= self.N:
            temp = self.q.get()
            if temp == 1 :
                self.c_hits -= 1
            elif temp == 2 :
                self.h_miss -= 1
        
        assert self.c_hits >= 0 and self.c_hits < self.N
        assert self.h_miss >= 0 and self.h_miss < self.N
        
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

