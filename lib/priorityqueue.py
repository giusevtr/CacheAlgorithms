'''
Created on Feb 10, 2018

@author: giuseppe
'''

class priorityqueue:
    def __init__(self, s):
        self.__capacity = s
        self.__key_locations = {}
        self.__freq = {}
        
        self.__heap = [None for _ in range(0, self.__capacity+1)]
        self.__size = 0
        
    def size(self):
        return self.__size
    
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
                self.__size -= 1
#                 print('debug i = ', i, self.__heap[i])
                self.__heapify(i)
        
    
    def increase(self, x):
        i = self.__key_locations[x]
        self.__freq[x] += 1
        self.__heapify(i)
       
    def __swap(self,i , j):
        tempi = self.__heap[i]
        tempj = self.__heap[j]
        self.__heap[i] = tempj
        self.__heap[j] = tempi
        self.__key_locations[tempj] = i
        self.__key_locations[tempi] = j
             
    
    def __heapify(self, i ):
        if 2*i+1 <= self.__size:
#             print('i = ',i)
            curr_key = self.__heap[i]
            left_key = self.__heap[2*i]
            right_key = self.__heap[2*i+1]
            if self.__freq[left_key] < self.__freq[right_key] :
                if self.__freq[left_key] < self.__freq[curr_key]:
                    self.__swap(i, 2*i)
                    self.__heapify(2*i)
            else:
                if self.__freq[right_key] < self.__freq[curr_key]:
                    self.__swap(i, 2*i+1)
                    self.__heapify(2*i+1)
        elif 2*i == self.__size:
            curr_key = self.__heap[i]
            left_key = self.__heap[2*i]
            if self.__freq[left_key] < self.__freq[curr_key]:
                self.__swap(i, 2*i)
                self.__heapify(2*i)
                    
    def __moveup(self,i):
        if i > 1 :
            par = i /2
#             print(par,i, ' ',self.__heap[par],self.__heap[i])
            freqi = self.__freq[self.__heap[i]]
            freqpar = self.__freq[self.__heap[par]]
            if freqi < freqpar:
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
        
if __name__ == "__main__" :
    
    pq = priorityqueue(30)
    
    pq.add(1)
    pq.add(2)
    pq.add(3)
    pq.add(4)
    pq.add(5)
    
    pq.increase(2)
    pq.increase(2)
    pq.increase(3)
    pq.increase(3)
    pq.increase(3)
    pq.increase(4)
    pq.increase(4)
    pq.increase(4)
    pq.increase(4)
    pq.increase(5)
    pq.increase(5)
    pq.increase(5)
    pq.increase(5)
    pq.increase(5)
    
    pq.debug()
    
    pq.increase(1)
    pq.increase(1)
    pq.increase(1)
    
    
    print(1 in pq)
    
    print(pq.peaktop())
#     pq.popmin()
#     pq.delete(1)
#     pq.delete(2)
#     print(pq.peaktop())
#     pq.popmin()
#     print(pq.peaktop())
    
    pq.debug()
    
    

        