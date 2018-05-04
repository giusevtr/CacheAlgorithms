from lib.CacheLinkedList import CacheLinkedList
import time
import numpy as np
import Queue
import heapq

class RecencyAndFrequencyCacheList:
    
    def __init__(self, N, visualization = True):
        self.N = N
        self.freq = {}
        self.PQ = []
        
        self.Cache = CacheLinkedList(N)
        self.Hist1 = CacheLinkedList(N)        
        self.Hist2 = CacheLinkedList(N)        
        
    def __contains__(self, page):
        return page in self.Cache
    
    def pageHitUpdate(self, page):
        self.cleanPQ()
        assert page in self.Cache and page in self.freq
        self.Cache.moveBack(page)
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
    
    def addToCache(self, page):
        self.cleanPQ()
        self.Cache.add(page)
        if page not in self.freq :
            self.freq[page] = 0
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
        
        
    def getHeapMin(self):
        while self.PQ[0][1] not in self.Cache or self.freq[self.PQ[0][1]] != self.PQ[0][0] :
            heapq.heappop(self.PQ) 
        return self.PQ[0][1]
    
    ######################
    ## Get LFU or LFU page
    ######################    
    def selectEvictPage(self, policy):
        self.cleanPQ()
        r = self.Cache.getFront()
        f = self.getHeapMin()
        
        pageToEvit,policyUsed = None, None
        if r == f :
            pageToEvit,policyUsed = r,-1
        elif policy == 0:
            pageToEvit,policyUsed = r,0
        elif policy == 1:
            pageToEvit,policyUsed = f,1
        
        return pageToEvit,policyUsed

    def evictPage(self, pg):
        assert pg in self.Cache
        self.Cache.delete(pg)
        
        
    def cleanPQ(self):
        if len(self.PQ) > 2*self.N:
            newpq = []
            for pg in self.Cache:
                newpq.append((self.freq[pg],pg))
            heapq.heapify(newpq)
            self.PQ = newpq
            del newpq
    
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
            del self.freq[histevict]
            return histevict
        return None
    
    def deleteHist1(self, page):
        self.Hist1.delete(page)
    
    def deleteHist2(self, page):
        self.Hist2.delete(page)
    
    def inHistory(self, page):
        return page in self.Hist1 or page in self.Hist2
    
    def inCache(self, page):
        return page in self.Cache
    
    
    