import random
import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import tensorflow as tf
import queue
from collections import deque
import numpy as np
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ExpertLearning(page_replacement_algorithm):

    def __init__(self, N):
        self.T = []
        self.N = N
        self.disk = Disk(N)
        self.freq = {}

        ## Training variables
        self.X, self.Y  = [], []
        self.reward = []
        self.regret = []

        ## Config variables
        self.batchsize = N
        self.numbatch = 5

        ## Aux variables
        self.hist = queue.deque()
        self.Xbuff = queue.deque()
        self.Ybuff = queue.deque()
        self.pageHitBuff = deque()

        self.current = 0
        self.action = 1
        self.currentPageHits = 0

        #self.discount = 0.9
        #self.sampleCount = 0
        #self.trainingSampleSize = 5 * N

    def get_N(self) :
        return self.N

    def __keyWithMinVal(self,d):
         v=list(d.values())
         k=list(d.keys())
         return k[v.index(min(v))]

    def __discountedReward(self, reward) :
        discounted_reward = np.zeros(len(reward))
        rsum = 0
        for t in reversed(range(0, len(reward))) :
            rsum = self.discount*rsum + reward[t]
            discounted_reward[t] = rsum
        return discounted_reward
    def __getRegret(self) :
        return 0

    def getState(self) :
        x = np.zeros(self.N, np.float32)
        for i, page in enumerate(self.disk) :
            x[i] = 1.0*self.freq[page]
        if np.sum(x) > 0.00001:
            x = x  / np.sum(x)
        return x

    def request(self,page) :
        page_fault = False

        ############################
        ## Save data for training ##
        ############################
        if self.current == 0 :
            ## Compute regret for the first batch
            if len(self.hist) == self.numbatch*self.batchsize :
                reg = self.__getRegret() ## Regret of first n pages
                x = self.Xbuff.popleft()
                y = self.Ybuff.popleft()
                h = self.pageHitBuff.popleft()

                ## Remove from hist and buffers
                for _ in range(0,self.N):
                    self.hist.get()
            ## Choose randomly
            self.action = 1 if np.random.rand() < 0.5 else 2
            self.Xbuff.append(self.getState())
            self.Ybuff.append(self.action)

        #########################
        ## Process page reques ##
        #########################
        if self.disk.inDisk(page) :
            self.disk.moveBack(page)
            self.freq[page] += 1
        else :
            if self.disk.size() == self.N :
                if self.action == 1 :
                    ## Remove LRU page
                    lru = self.disk.getIthPage(0)
                    self.disk.delete(lru)
                    del self.freq[lru]
                elif self.action == 2 :
                    ## Remove LFU page
                    lfu = self.__keyWithMinVal(self.freq)
                    self.disk.delete(lfu)
                    del self.freq[lfu]

            # Add page to the MRU position
            self.disk.add(page)
            self.freq[page] = 1
            page_fault = True

        ## Increate page hits counter
        self.currentPageHits += 1*(not page_fault)

        ## Save page hits for current batch
        if self.current + 1 == self.batchsize :
            self.pageHitBuff.append(self.currentPageHits)

        ## Save page in history
        self.hist.put(page)

        ## Increase batch size counter
        self.current = (self.current + 1 ) % self.batchsize

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
