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
class OLCR(page_replacement_algorithm):

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
        
        input_units = 2*self.N
        hidden_units = 2
        output_units = 1
        
        self.X = tf.placeholder(dtype=tf.int32, shape=[None,2])
        self.P = tf.placeholder(dtype=tf.float32, shape=[None,1])
        
        self.C_r = tf.placeholder(dtype=tf.float32, shape=[None])
#         self.C_f = tf.placeholder(dtype=tf.float32, shape=[None])
        
        self.W = tf.Variable(tf.random_uniform([input_units, hidden_units]))
        self.b = tf.Variable(tf.ones([hidden_units]))
        
        self.W_hidden   = tf.Variable(tf.random_uniform([hidden_units, output_units]))
        self.b_hidden   = tf.Variable(tf.ones([output_units]))
        
        
        
#         self.predict = tf.sigmoid(tf.matmul(self.X, self.W))
#         self.predict = tf.sigmoid(tf.slice(self.W, self.X[0,0],[1]) + tf.slice(self.W, self.X[0,1]+self.N,[1]))
        idx1 = tf.slice(self.X,[0,0],[-1,1])
        idx2 = tf.slice(self.X,[0,1],[-1,1]) + self.N
        
        ## Neuron 1
#         self.w1 = tf.slice(self.W, [0, idx1[0]],[1,1])
#         self.w2 = tf.slice(self.W, [0, idx2[0]+self.N,[1])
        
        
        self.w11 = tf.slice(self.W, [self.X, 0],[1,1])
        
        self.w11 = tf.gather(self.W, self.idx1)
        self.w22 = tf.gather(self.W, self.idx2+self.N)
        
        
        self.w22 = tf.slice(self.W, [idx2[0,0]+self.N,1],[1,1])
        
        self.w13 = tf.slice(self.W, [2, idx1[0,0]],[1,1])
        self.w23 = tf.slice(self.W, [2, idx2[0,1]+self.N],[1,1])
        
        
        
        ## Hidden layer
        self.neuron1 = tf.sigmoid(self.w11 + self.b[0]) # only x1
        self.neuron2 = tf.sigmoid(self.w22 + self.b[1]) # only x2
        self.neuron3 = tf.sigmoid(self.w13 + self.w13 + self.b[2])# x1+x2
        
        self.logit1 = tf.contrib.layers.flatten(tf.concat([self.neuron1, self.neuron2,self.neuron3], 1)) # 1 x hidden_units 
        
        self.logit2 = tf.sigmoid(tf.matmul(self.logit1,self.W_hidden) + self.b_hidden)
        
        
#         self.predict =  tf.nn.softmax(self.logit2)
        self.predict = self.logit2
        
        self.cost = -tf.reduce_mean(self.C_r * tf.log(1-self.predict) + (1-self.C_r) * tf.log(self.predict))
        learning_rate = 0.1
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)
        
        ##################################
        self.X_holder = []
        self.P_holder = []
        self.R_holder = []
        self.F_holder = []
        self.train_batch_size = self.N/4
        
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
        
        assert len(self.PQ) >= self.N, 'PQ should be full %d' % len(self.PQ)
        while self.PQ[0][1] not in self.CacheRecency or self.freq[self.PQ[0][1]] != self.PQ[0][0] :
            heapq.heappop(self.PQ) 
        return self.PQ[0][1]
    
    ######################
    ## Get LFU or LFU page
    ## return page, poly
    ######################    
    def selectEvictPage(self, P):
        assert P >= 0 and P <= 1.1, 'P = %f' % P
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
        
        #######################
        ## Train
        #######################
        if len(self.X_holder) >= self.train_batch_size:
            
            X_1 = np.array(self.X_holder)
            
#             t1 = tf.one_hot(X_1[:,0], depth=self.N)
#             t2 = tf.one_hot(X_1[:,1], depth=self.N)
#             X_2 = tf.concat([t1,t2], 1)
            
#             print 'cost = %f' % self.sess.run(self.cost,  feed_dict={   self.X:X_1, 
#                                                         self.C_r:np.array(self.R_holder),
#                                                         self.C_f:np.array(self.F_holder)})
            
            self.sess.run(self.optimizer, feed_dict={   self.X:X_1, 
                                                        self.C_r:np.array(self.R_holder)})
            self.X_holder = []
            self.P_holder = []
            self.R_holder = []
            self.F_holder = []
        
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
            page_outcome = -1
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            
            if page in self.Hist1 or page in self.Hist2:
                page_outcome = 1
                
                X = self.param[page]
                P = self.pUsed[page]
                e = self.error_discount_rate ** (self.time - self.evictionTime[page])
                
                ## TODO Consider dividing e by P
                self.X_holder.append(X)
                self.P_holder.append(P)
                self.R_holder.append(e)
                
                if page in self.Hist1 :
                    self.Hist1.delete(page)
#                     self.R_holder.append(e)
#                     self.F_holder.append(0)
                else:
                    self.Hist2.delete(page)
#                     self.R_holder.append(0)
#                     self.F_holder.append(e)
            else :
                page_outcome = 2 
            ####################
            ## Remove from Cache
            ####################
            if self.CacheRecency.size() == self.N:
                
                ################
                ## Choose Policy
                ################
                
#                 t1 = tf.one_hot([self.c_hits], depth=self.N)
#                 t2 = tf.one_hot([self.h_miss], depth=self.N)
#                 X_2 = tf.concat([t1,t2], 1)
                
                P = self.sess.run(self.predict, feed_dict={self.X:np.array([[self.c_hits, self.h_miss]])})[0,0]
                
#                 print self.sess.run(self.unnormweight,feed_dict={self.X:np.array([[self.c_hits, self.h_miss]])})
#                 print 'P = ', P
                
                
#                 assert np.sum(P) <= 1.0, np.sum(P)
                
#                 P = np.random.rand()
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

