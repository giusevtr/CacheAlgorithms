import random
import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import tensorflow as tf
import queue
from collections import deque
import numpy as np
from collections import Counter
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

class dequecustom(deque) :
    def getleft(self) :
        x = self.popleft()
        self.appendleft(x)
        return x

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ExpertLearning_v2(page_replacement_algorithm):

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
        self.discountrate = 0.9
        self.error = 0.5
        self.reduceErrorRate = 0.975

        ## Aux variables
        self.cachebuff = dequecustom()
        self.Xbuff = dequecustom()
        self.Ybuff = dequecustom()
        self.pageHitBuff = dequecustom()
        self.hist = dequecustom()
        self.batchsizeBuff = dequecustom()

        ## Accounting variables
        self.currentPageHits = 0
        self.current = 0
        self.uniquePages = Counter()

        ## Batch action variable
        self.action = [0]

        #self.discount = 0.9
        #self.sampleCount = 0
        #self.trainingSampleSize = 5 * N

        ## start tf
        tf.reset_default_graph()

        self.input = tf.placeholder(shape=[1,self.N], dtype=tf.float32)
        W1 = tf.Variable(tf.random_uniform([self.N,8],0,0.01))
        out1 = tf.sigmoid(tf.matmul(self.input, W1))
        W2 = tf.Variable(tf.random_uniform([8,2],0,0.01))
        self.out = tf.matmul(out1, W2)
        self.predictaction = tf.argmax(self.out)

        self.nextQ = tf.placeholder(shape=[1,2], dtype=tf.float32)
        loss = tf.reduce_sum(tf.square(self.out - self.nextQ))
        trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
        self.updatemodel = trainer.minimize(loss)

        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

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
        cache = set(self.cachebuff.getleft())
        requestSequence = list(self.hist)

        ## Compute distance
        dist = {}
        for j, p in enumerate(requestSequence):
            if p not in dist :
                dist[p] = dequecustom()
            dist[p].append(j)

        discountedregret = 0

        i = 0
        batchid = 0
        optsum = 0
        hitsum = 0
        for hits, sz in zip(self.pageHitBuff, self.batchsizeBuff) :
            opthits = 0
            batchid += 1
            for _ in range(0, sz) :
                p = requestSequence[i]
                i += 1
                if p in cache :
                    opthits += 1
                else :
                    if len(cache) >= self.N :
                        rem = 'xxxxxxxxxxxxx'
                        for c in cache :
                            if c not in dist or len(dist[c]) == 0:
                                rem = c
                                break
                            if rem not in dist or dist[c].getleft() > dist[rem].getleft():
                                rem = c
                        ## Evict from cache
                        cache = cache - {rem}
                    ## Add page to cache
                    cache = cache | {p}
                ## Pop from dist
                dist[p].popleft()

            regret = opthits - hits
            discountedregret = discountedregret + regret * (0.9) ** (batchid-1)
            optsum += opthits
            hitsum += hits
            break

        return discountedregret

    def getState(self) :
        x = np.zeros(self.N, np.float32)
        for i, page in enumerate(self.disk) :
            x[i] = 1.0*self.freq[page]
        if np.sum(x) > 0.00001:
            x = x  / np.sum(x)
        return x

    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False

        ############################
        ## Save data for training ##
        ############################
        if len(self.uniquePages) == 0 :
            ## Compute regret for the first batch

            if len(self.Xbuff) >= self.numbatch :
                r = self.__getRegret()
                cache = self.cachebuff.popleft()
                s1 = np.array(self.Xbuff.popleft())
                s2 = np.array(self.Xbuff.getleft())
                act = self.Ybuff.popleft()
                hits = self.pageHitBuff.popleft()
                sz = self.batchsizeBuff.popleft()
                for _ in range(0,sz):
                    temp = self.hist.popleft()

                #############################################################################################################################
                ## Train here ###############################################################################################################
                #############################################################################################################################
                allq = self.sess.run(self.out,feed_dict={self.input:s1})
                nextq  = self.sess.run(self.out,feed_dict={self.input:s2})
                Qmax = np.max(nextq)
                targetQ = allq
                targetQ[0, act[0]] = r + self.discountrate*Qmax

                _  = self.sess.run(self.updatemodel,feed_dict={self.input: s1, self.nextQ : targetQ})
                #self.error = self.error * self.reduceErrorRate

            #####################
            ## Choose randomly ##
            #####################
            state = np.array([self.getState()])
            #print(state)
            self.action = self.sess.run(self.predictaction,feed_dict={self.input:state})

            if np.random.rand() < self.error :
                self.action[0] = 0 if np.random.rand() < 0.5 else 1

            self.cachebuff.append(self.disk.getData())
            self.Xbuff.append(state)
            self.Ybuff.append(self.action)

        #########################
        ## Process page reques ##
        #########################
        if self.disk.inDisk(page) :
            self.disk.moveBack(page)
            self.freq[page] += 1
            self.currentPageHits += 1
        else :
            if self.disk.size() == self.N :
                if self.action[0] == 0 :
                    ## Remove LRU page
                    lru = self.disk.getIthPage(0)
                    self.disk.delete(lru)
                    del self.freq[lru]
                elif self.action[0] == 1 :
                    ## Remove LFU page
                    lfu = self.__keyWithMinVal(self.freq)
                    self.disk.delete(lfu)
                    del self.freq[lfu]
            # Add page to the MRU position
            self.disk.add(page)
            self.freq[page] = 1
            page_fault = True

        #self.uniquePages = self.uniquePages | {page}
        self.uniquePages.update({page:1})

        ## Store page hits for current batch
        if len(self.uniquePages) == self.N :
            self.pageHitBuff.append(self.currentPageHits)
            self.batchsizeBuff.append(sum(self.uniquePages.values()))
            ## Reset variables
            self.uniquePages.clear()
            self.currentPageHits = 0

        self.hist.append(page)

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
