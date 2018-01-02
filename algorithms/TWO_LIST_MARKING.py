import sys
import random
from marking_func import *
from lib.disk_struct import Disk

class TWO_LIST_MARKING:

    def __init__(self, N):
        self.M1 = Disk(N)
        self.M2 = Disk(N)
        self.U1 = Disk(N)
        self.U2 = Disk(N)
        self.B1 = Disk(N)
        self.B2 = Disk(N)
        self.P = 0

        self.N = N
    def get_N(self) :
        return self.N

    def request(self,page) :
        pageFault = False;
        if self.M1.inDisk(page) or self.M2.inDisk(page) or self.U1.inDisk(page) or self.U2.inDisk(page) :

            ## Remove from the list
            self.M1.delete(page)
            self.M2.delete(page)
            self.U1.delete(page)
            self.U2.delete(page)

            ## Move to M2
            self.M2.add(page)
        else :
            pageFault = True
            ## Start a new phase when all pages are marked and a page fault occurs
            if self.M1.size() + self.M2.size() == self.N :
                m1_data = self.M1.getData()
                m2_data = self.M2.getData()
                for x in m1_data :
                    self.M1.delete(x)
                    self.U1.add(x)
                for x in m2_data :
                    self.M2.delete(x)
                    self.U2.add(x)

            ## If page is in history then update P
            ## u = u1 + u2
            ## 0 <= p <= u / u1
            ## p(u1) = p / u
            ## p(u2) = (u - p*u1)/(u*u2)
            u1 =  self.U1.size()
            u2 =  self.U2.size()
            u = u1 + u2
            if self.B1.inDisk(page) :
                if u1 > 0 :
                    self.P += 1.0 * u2 / u1
                else :
                    self.P += 0.5

                if u1 > 0 and self.P > (u / u1) :
                    self.P = (u / u1)

                self.B1.delete(page)
            elif self.B2.inDisk(page):
                if u2 > 0 :
                    self.P -= 1.0 * u1 / u2
                else :
                    self.P -= 0.5

                if self.P < 0 :
                    self.P = 0
                self.B2.delete(page)


            if self.M1.size() + self.M2.size() + self.U1.size() + self.U2.size() == self.N:
                # Evict a page
                U1 = self.U1.getData()
                U2 = self.U2.getData()

                if u1 == 0 :
                    p1 = 0
                    p2 = 1.0/u
                elif u2 == 0:
                    p1 = 1.0/u
                    p2 = 0
                else :
                    p1 = self.P / u                         # Probability of choosing a page in U1
                    p2 = (u - self.P * u1) / (u * u2)       # Probability of choosing a page in U2

                ## Calculate probability distribution
                P = [0 for i in range(0,self.N)]
                for i,u in enumerate(U1) :
                    P[i] = p1
                    if i > 0 :
                        P[i] += P[i-1]
                for i,u in enumerate(U2) :
                    P[i + u1] = p2
                    if i + u1 > 0  :
                        P[i+u1] += P[i+u1-1]

                ## Choose a page a random
                ran = random.random()
                U = U1 + U2
                for i,u in enumerate(U) :
                    if ran < P[i] :
                        self.U1.delete(u)
                        self.U2.delete(u)
                        evicted = u
                        if i < u1 :
                            inU1 = True
                        else :
                            inU1 = False
                        break

                if inU1 :
                    if self.B1.size() == self.N :
                        self.B1.deleteFront()
                    self.B1.add(evicted)
                else :
                    if self.B2.size() == self.N :
                        self.B2.deleteFront()
                    self.B2.add(evicted)

            ## Add new page to M1
            self.M1.add(page)

            return pageFault

    def getData(self):
        m1 = []
        m2 = []
        u1 = []
        u2 = []
        b1 = []
        b2 = []


        for m in self.M1.getData() :
            m1.append((m,1))
        for m in self.M2.getData() :
            m2.append((m,3))
        for u in self.U1.getData() :
            u1.append((u,0))
        for u in self.U2.getData() :
            u2.append((u,2))
        for m in self.B1.getData() :
            b1.append(m)
        for m in self.B2.getData() :
            b2.append(m)

        return [u1+m1+u2+m2,b1,b2]


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print("Error: Must supply cache size.")
        print("usage: python3 [cache_size]")
        exit(1)

    n = int(sys.argv[1])
    print("cache size ", n)

    marking = TWO_LIST_MARKING(n)
    page_fault_count = 0
    page_count = 0
    for line in sys.stdin:
        #print("request: ", line)
        if marking.request(line) :
            page_fault_count += 1
        page_count += 1


    print("page count = ", page_count)
    print("page faults = ", page_fault_count)
