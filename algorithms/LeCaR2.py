from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.RecencyAndFrequencyCacheList import RecencyAndFrequencyCacheList
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
class LeCaR2(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.Cache = RecencyAndFrequencyCacheList(N)
      
        
        ## Config variables
        self.error_discount_rate = (0.005)**(1.0/N)
        
        ####################################################################################################################        
        self.evictionTime = {}
        self.stateAction = {}
        self.time = 0
        ####################################################################################################################        
        
        ####################################################################################################################        
        ## State variables:
        ####################################################################################################################        
        self.q = Queue.Queue()
        self.sum = 0
        self.NewPages = []
        self.NewPages = 0
        self.FromHr = 0
        self.FromHf = 0
        self.PageType = {}
        ####################################################################################################################        
        ####################################################################################################################        

        
        
        ####################################################################################################################
        ## Tensorflow
        ####################################################################################################################        
        self.discount_rate = 0.95
        self.state_dimensions = 3
        self.actions_dimensions = 5
        
        self.cacheState = tf.placeholder(dtype=tf.float32, shape=[self.state_dimensions])
        self.newCost = tf.placeholder(dtype=tf.float32, shape=[self.actions_dimensions])
        
        self.actionCost = tf.contrib.layers.full_connected(self.cacheState, self.actions_dimensions, activation = None,weights_initializer=tf.ones_initializer())  # Linear activation
        self.actionCost = tf.reshape(self.actionCost,[-1])
        
        self.bestAction = tf.argmin(self.actionCost)
        
        self.loss = tf.reduce_sum(tf.square(self.newCost - self.actionCost))
        
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
        
        self.Update = optimizer.minimize(self.loss)
        
        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)
        

        
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        return []
    
    def getState(self):
        return [self.NewPages, self.FromHr, self.FromHf]
        
    
    def updateWeights(self, s, s1, act, cost):
        ac = self.sess.run(self.actionCost, feed_dict={self.cacheState : s})
        predicted = self.sess.run(self.actionCost, feed_dict={self.cacheState : s1})
        ac[act] = cost + self.discount_rate * np.min(predicted)
        self.sess.run(self.update, feed_dict={self.newCost: ac, self.cacheState : s})
        
        
    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self):
        r = np.random.rand()
        if r < self.W[0] :
            return 0
        return 1
            
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        
        page_outcome = -1
        
        ##########################
        ## Process page request 
        ##########################
        if page in self.Cache:
            page_fault = False
            self.Cache.pageHitUpdate(page)
            page_outcome = -1
            
            if self.PageType[page] == 'New' :
                self.NewPages -= 1
                self.PageType[page] = 'None'
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            
            if self.Cache.inHistory(page):
                page_outcome = 1
                
                X = self.param[page]
                P = self.pUsed[page]
#                 e = self.error_discount_rate ** (self.time - self.evictionTime[page])
                
                ## TODO Consider dividing e by P
                self.X_holder.append(X)
                self.P_holder.append(P)
                
                if page in self.Hist1:
                    self.Cache.deleteHist1(page)
                    self.R_holder.append(1)
                    self.F_holder.append(0)
                    self.FromHr += 1
                    self.PageType[page] = 'Hr'
                else :
                    self.Cache.deleteHist2(page)
                    self.R_holder.append(0)
                    self.F_holder.append(1)
                    self.FromHf += 1
                    self.PageType[page] = 'Hf'
            else :
                page_outcome = 2 
                self.NewPages += 1
                self.PageType[page] = 'New'
            
            
            ####################
            ## Update weights
            ####################
            
            
            
            ####################
            ## Remove from Cache
            ####################
            if self.Cache.Cache.size() == self.N:
                
                ################
                ## Choose Policy
                ################
                if np.random.rand() < 0.5 :
                    actions = self.sess.run(self.actionCost, feed_dict={self.X:np.array([[self.c_hits, self.h_miss]])})[0,0]
                    a = np.argmax(actions, 0)
                else :
                    a = np.random.randint(10)
                    
                P = a * 1.0 / (self.actions_dimensions-1)
                
#                 print self.sess.run(self.unnormweight,feed_dict={self.X:np.array([[self.c_hits, self.h_miss]])})
#                 print 'P = ', P
                
                
#                 assert np.sum(P) <= 1.0, np.sum(P)
                
#                 P = np.random.rand()
                cacheevict,poly = self.Cache.selectEvictPage(P)
                
                self.evictionTime[cacheevict] = self.time
                self.stateAction[cacheevict] = [self.getState(), a]
                
                
                
                ###################
                ## Remove from Cache and Add to history
                ###################
                self.Cache.evictPage(cacheevict)
                self.Cache.addToHistory(poly, cacheevict)
                
                if self.PageType[cacheevict] == 'Hr' :
                    self.FromHr -= 1
                if self.PageType[cacheevict] == 'Hf' :
                    self.FromHf -= 1
                if self.PageType[cacheevict] == 'New' :
                    self.NewPages -= 1
                del self.PageType[cacheevict]
                
                
                
                self.Cache.addToCache(page)
                
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

