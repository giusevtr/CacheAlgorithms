'''
Created on Feb 10, 2018

@author: giuseppe
'''
from lib.CacheDataStruct import CacheDataStruct

class priorityqueue(CacheDataStruct):
    def __init__(self, s, decay = 0.99):
        self.__capacity = s
        self.__key_locations = {}
        self.__freq = {}
        self.__accesstime = {}
        self.__heap = [None for _ in range(0, self.__capacity+1)]
        self.__size = 0
        self.time = 0
        self.__decaytime = self.__capacity

    def getFreqDic(self):
        return self.__freq
        
    def size(self):
        return self.__size

    def getCount(self, page):
        return self.getFreq(page)

    def getFreq(self, page):
        if page in self.__freq:
            return self.__freq[page]
        return None

    def decay(self, decay_factor):
        for pg in self.__freq:
            self.__freq[pg] /= decay_factor
            self.__freq[pg] = int(self.__freq[pg]+0.5) # round up so that no page has frequency equals to 0

    def peaktop(self):
        if self.__size == 0 :
            return None
        return self.__heap[1]

    def popmin(self):
        if self.__size == 0 :
            return None
        ret = self.__heap[1]
        self.delete(ret)
        return ret

    def add(self, x):
        if x not in self.__freq and self.__size < self.__capacity :
            self.__size += 1
            self.__heap[self.__size] = x
            self.__key_locations[x] = self.__size
            self.__freq[x] = 1
            self.__settime(x)
            self.__moveup(self.__size)

        elif x in self.__freq:
            self.increase(x)

    def delete(self, x):
        if x in self.__key_locations :
            i = self.__key_locations[x]
            if self.__size>0 and i <= self.__size:
                self.__swap(i, self.__size)
                self.__heap[self.__size] = None
                del self.__key_locations[x]
                del self.__freq[x]
                del self.__accesstime[x]
                self.__size -= 1
                self.__heapify(i)
        if x in self.__freq:
            del self.__freq[x]
        if x in self.__accesstime:
            del self.__accesstime[x]

    def __settime(self,x):
        self.__accesstime[x] = self.time
        self.time +=1

    def increase(self, x, amount = 1):
        i = self.__key_locations[x]
        self.__freq[x] += amount
        self.__settime(x)
        self.__heapify(i)

    def __swap(self,i , j):
        tempi = self.__heap[i]
        tempj = self.__heap[j]
        self.__heap[i] = tempj
        self.__heap[j] = tempi
        self.__key_locations[tempj] = i
        self.__key_locations[tempi] = j

    ## True if key1 comes before key2
    def __comparekeys(self, key1, key2):
        if self.__freq[key1] == self.__freq[key2] :
            return self.__accesstime[key1] < self.__accesstime[key2]
        return self.__freq[key1] < self.__freq[key2]

    def __heapify(self, i ):
        if 2*i+1 <= self.__size:
#             print('i = ',i)
            curr_key = self.__heap[i]
            left_key = self.__heap[2*i]
            right_key = self.__heap[2*i+1]
            #if self.__freq[left_key] < self.__freq[right_key] :
            if self.__comparekeys(left_key, right_key):
                #if self.__freq[left_key] < self.__freq[curr_key]:
                if self.__comparekeys(left_key, curr_key):
                    self.__swap(i, 2*i)
                    self.__heapify(2*i)
            else:
                #if self.__freq[right_key] < self.__freq[curr_key]:
                if self.__comparekeys(right_key, curr_key):
                    self.__swap(i, 2*i+1)
                    self.__heapify(2*i+1)
        elif 2*i == self.__size:
            curr_key = self.__heap[i]
            left_key = self.__heap[2*i]
            #if self.__freq[left_key] < self.__freq[curr_key]:
            if self.__comparekeys(left_key, curr_key) :
                self.__swap(i, 2*i)
                self.__heapify(2*i)

    def __moveup(self,i):
        if i > 1 :
            par = i /2
#             print(par,i, ' ',self.__heap[par],self.__heap[i])
            if self.__comparekeys(self.__heap[i], self.__heap[par]):
                self.__swap(par, i)
                self.__moveup(par)

    def __contains__(self, x):
        return x in self.__freq

    def debug(self):
#         print(self.__heap)
        L = []
        for h in self.__heap:
            if h is not None:
                L.append(self.__freq[h])
        print(L)

    def getData(self):
        return self.__freq.keys()

if __name__ == "__main__" :

    pq = priorityqueue(30)

    pq.add(1)
    pq.add(2)
    pq.add(3)
    pq.add(4)
    pq.add(5)


    print(pq.popmin())
    print(pq.popmin())
    pq.add(5)
    pq.add(4)
    pq.add(3)

    print(pq.popmin())
    print(pq.popmin())
    pq.add(1)
    pq.add(1)
    print(pq.popmin())




#     pq.increase(2)
#     pq.increase(2)
#     pq.increase(3)
#     pq.increase(3)
#     pq.increase(3)
#     pq.increase(4)
#     pq.increase(4)
#     pq.increase(4)
#     pq.increase(4)
#     pq.increase(5)
#     pq.increase(5)
#     pq.increase(5)
#     pq.increase(5)
#     pq.increase(5)
#     pq.debug()
#     pq.increase(1)
#     pq.increase(1)
#     pq.increase(1)
#     print(1 in pq)
#     print(pq.peaktop())
# #     pq.popmin()
# #     pq.delete(1)
# #     pq.delete(2)
# #     print(pq.peaktop())
# #     pq.popmin()
# #     print(pq.peaktop())
#
#     pq.debug()
