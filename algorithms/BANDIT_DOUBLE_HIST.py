from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import numpy as np
# import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class BANDIT_DOUBLE_HIST(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.Cache = Disk(N)
        self.Hist1 = Disk(N)        
        self.Hist2 = Disk(N)        
        
        ## Config variables
        self.decayRate = 0.99
        self.epsilon = 0.95
        self.lamb = 0.05
        self.learning_phase = N/2
        self.error_discount_rate = (0.005)**(1.0/N)
        ## 
        self.learning = True
        self.policy = 0
        self.accessedTime = {}
        self.frequency = {}
        self.evictionTime = {}
        self.policyUsed = {}
        self.weightsUsed = {}
        ## Accounting variables
        self.time = 0
        
        self.W = np.array([.5,.5], dtype=np.float32)
        
        self.X = np.array([])
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        print('visualize')
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W_lru')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W_lfu')
        plt.xlabel('time')
        plt.ylabel('Weight')
        plt.legend(handles=[l1,l2])
#         plt.show()
        
#         print('W = ', self.W)
    def __keyWithMinVal(self,d):
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(min(v))]
    
    def getMinValueFromCache(self, values):
        minpage,first = -1, True
        for q in self.Cache :
            if first or values[q] < values[minpage] :
                minpage,first=q,False
        return minpage
    
    def selectEvictPage(self, policy):
        r = self.getMinValueFromCache(self.accessedTime)
        f = self.getMinValueFromCache(self.frequency)
        
#         if r == f :
#             return r,-1
        if policy == 0:
            return r,0
        return f, 1
    
    def countUniquePagesSince(self, t):
        cnt = 0
        for p in self.Cache :
            if self.accessedTime[p] > t :
                cnt += 1
        for p in self.Hist1 :
            if self.accessedTime[p]>t :
                cnt +=1
        for p in self.Hist2 :
            if self.accessedTime[p]>t :
                cnt +=1
                    
        return cnt
        
    def getQ(self):
        return (1-self.lamb) * self.W + self.lamb*np.ones(2)/2
#         return self.W

    def chooseRandom(self):
        q = self.getQ()
        
        r = np.random.rand()
        
        
#         if self.time < 10000 + 1751 and self.time > 1751:
#             print('r = ', r, 'q = ', q)
                
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
        ############################
        ## Save data for training ##
        ############################

        if self.time % self.learning_phase == 0 :
            self.learning = not self.learning
        
        ## Visualization data
        prob = self.getQ()
        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, prob[0])
        self.Y2 = np.append(self.Y2, prob[1])

        #########################
        ## Process page reques ##
        #########################
        if page in self.Cache:
            page_fault = False
        else :
            
            pageevict = None
            policyUsed = -1
            if page in self.Hist1:
                pageevict = page
                self.Hist1.delete(page)
                policyUsed = 0
            elif page in self.Hist2:
                pageevict = page
                self.Hist2.delete(page)
                policyUsed = 1
                
            if pageevict is not None :
                q = self.weightsUsed[pageevict]
                
                err = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                reward = np.array([0,0], dtype=np.float32)
                if policyUsed == 0 :
                    reward[1] = err
                if policyUsed == 1:
                    reward[0] = err
                
                reward_hat = reward / q
                
#                 print('self.policyUsed[%d] = %d' % (pageevict,self.policyUsed[pageevict] ))
                ## Update Weights
                if self.policyUsed[pageevict] != -1 :
#                     print('Updating weights')
                    self.W = self.W * np.exp(self.lamb * reward_hat / 2)
                    self.W = self.W / np.sum(self.W)
                
                
            ## Remove from Cache
            if self.Cache.size() == self.N:
                if  not self.learning :
                    act = np.argmax(self.getQ())
                else :
                    act = self.chooseRandom()
                
                
                
#                 act = self.chooseRandom()
                
                cacheevict,poly = self.selectEvictPage(act)
                self.policyUsed[cacheevict] = poly
                
#                 if self.time < 10000 + 1751 and self.time > 1751:
#                     if act == 1 :
#                         print('LFU')
                        
                if not self.learning :
                    self.policyUsed[cacheevict] = -1
                
                self.Cache.delete(cacheevict)
                
                self.weightsUsed[cacheevict] = self.getQ()
                self.evictionTime[cacheevict] = self.time
                
                histevict = -1
                if act == 0:
                    if self.Hist1.size() == self.N :
                        histevict = self.Hist1.getIthPage(0)
                        self.Hist1.delete(histevict)
                    self.Hist1.add(cacheevict)
#                     print('Adding %d to hist1' % cacheevict)
                if act == 1:
                    if self.Hist2.size() == self.N :
                        histevict = self.Hist2.getIthPage(0)
                        self.Hist2.delete(histevict)
                    self.Hist2.add(cacheevict)
#                     print('Adding %d to hist2' % cacheevict)
                
                if histevict != -1 :
                    del self.evictionTime[histevict]
                    del self.accessedTime[histevict]
                    del self.frequency[histevict]
                    del self.policyUsed[histevict]
                    del self.weightsUsed[histevict]
#                 print('act = ', act)
#                 self.Hist.add(evictPage)
                
                    
            if page not in self.frequency:
                self.frequency[page] = 0
            self.Cache.add(page)
            page_fault = True

        for q in self.Cache :
            self.frequency[q] *= self.decayRate
        self.frequency[page] += 1
        self.accessedTime[page] = self.time
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

