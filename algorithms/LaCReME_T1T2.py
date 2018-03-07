from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
import numpy as np
import Queue
# import matplotlib.pyplot as plt
import os
from scipy.constants.constants import alpha
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LaCReME_T1T2(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.T1 = Disk(N)
        self.T2 = Disk(N)
        
        self.Hist1 = Disk(N)        
        self.Hist2 = Disk(N)        
        
        ## Config variables
        self.epsilon = 0.90
        self.lamb = 0.05
        self.error_discount_rate = (0.005)**(1.0/N)
#         self.learning_phase = N/2
#         self.error_discount_rate = 1
        
        ## 
        self.policy = 0
        self.evictionTime = {}
        self.policyUsed = {}
        self.weightsUsed = {}
        self.freq = {}
        
        ## TODO add decay_time and decay_factor
        self.decay_time = N
        self.decay_factor = 1
        
        ## Accounting variables
        self.time = 0
        
        self.W = np.array([.5,.5], dtype=np.float32)
        
        self.X = np.array([],dtype=np.int32)
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        
        
        ###
        self.q = Queue.Queue()
        self.sum = 0
        self.NewPages = []
        
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
#         print(np.min(self.X), np.max(self.X))
        ax = plt.subplot(2,1,1)
        ax.set_xlim(np.min(self.X), np.max(self.X))
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W_lru')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W_lfu')
        l3, = plt.plot(self.X, self.NewPages, 'g-', label='New Pages', alpha=0.6)
        return [l1,l2,l3]
    
    ##############################################################
    ## There was a page hit to 'page'. Update the data structures
    ##############################################################
    def pageHitUpdate(self, page):
        if page in self.T1:
            self.T1.delete(page)
            self.T2.add(page)
        else :
            self.T2.moveBack(page)
        
    #########################
    ## Get the Q distribution
    #########################
    def getQ(self):
        return (1-self.lamb) * self.W + self.lamb*np.ones(2)/2
    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self):
        q = self.getQ()
        r = np.random.rand()
        for i,p in enumerate(q):
            if r < p:
                return i 
        return len(q)-1
    def updateWeight(self, cost):
        self.W = self.W * (1-self.epsilon * cost)
        self.W = self.W / np.sum(self.W)
    
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
#         if self.time % self.learning_phase == 0 :
#             self.learning = not self.learning
        
        #####################
        ## Visualization data
        #####################
        prob = self.getQ()
        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, prob[0])
        self.Y2 = np.append(self.Y2, prob[1])
        notInHistory = 0
        
        ##########################
        ## Process page request 
        ##########################
        t1 = self.T1.size()
        t2 = self.T2.size()
        assert t1 + t2 <= self.N
        if page in self.T1 or page in self.T2:
            page_fault = False
            self.pageHitUpdate(page)
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            pageevict = None
            inHist = False
            policyUsed = -1
            
            if page in self.Hist1:
                pageevict = page
                self.Hist1.delete(page)
                policyUsed = 0
                inHist = True
            elif page in self.Hist2:
                pageevict = page
                self.Hist2.delete(page)
                policyUsed = 1
                inHist = True
            else:
                notInHistory = 1
                
            if pageevict is not None :
                q = self.weightsUsed[pageevict]
#                 err = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                err = 1
                reward = np.array([0,0], dtype=np.float32)
                if policyUsed == 0 : # LRU
                    reward[1] = err
                if policyUsed == 1:
                    reward[0] = err
                reward_hat = reward / q
                
                #################
                ## Update Weights
                #################
                if self.policyUsed[pageevict] != -1 :
                    self.W = self.W * np.exp(self.lamb * reward_hat / 2)
                    self.W = self.W / np.sum(self.W)
            
            ####################
            ## Remove from Cache
            ####################
            if t1 + t2 == self.N:
                
                ################
                ## Choose Policy
                ################
                
                act = self.chooseRandom()                
                if t1 == self.N or (act == 0 and t1 > 0):
                    cacheevict = self.T1.popFront()
                else :
                    cacheevict = self.T2.popFront()
                
                self.policyUsed[cacheevict] = act
                self.weightsUsed[cacheevict] = self.getQ()
                self.evictionTime[cacheevict] = self.time
                
                ###################
                ## Evict to history
                ###################
                histevict = None
                if act == 0:
                    if self.Hist1.size() == self.N :
                        histevict = self.Hist1.getFront()
                        self.Hist1.delete(histevict)
                    self.Hist1.add(cacheevict)
                else:
                    if self.Hist2.size() == self.N :
                        histevict = self.Hist2.getFront()
                        self.Hist2.delete(histevict)
                    self.Hist2.add(cacheevict)
                
                if histevict is not None :
                    del self.evictionTime[histevict]
                    del self.policyUsed[histevict]
                    del self.weightsUsed[histevict]
                
            
            if inHist :
                self.T2.add(page)
            else :
                self.T1.add(page)
                    
            page_fault = True

        self.q.put(notInHistory)
        self.sum += notInHistory
        if self.q.qsize() > self.N:
            self.sum -= self.q.get()
        
        self.NewPages.append(1.0*self.sum / self.N)
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

