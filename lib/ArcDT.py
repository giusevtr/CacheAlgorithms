'''
Created on Feb 26, 2018

@author: giuseppe
'''
from disk_struct import Disk 

class ArcDT:
    def __init__(self,N):
        self.N = N
        self.T1 = Disk(N)
        self.T2 = Disk(N)
        self.B1 = Disk(N)
        self.B2 = Disk(2*N)
        self.P = 0
        self.__freq = {}
        
    def increaseCount(self, page, amount =1):
        if page in self.__freq:
            self.__freq[page] += 1
    def getCount(self, page):
        return self.__freq[page]
    def setCount(self, page, cnt):
        self.__freq[page] = cnt
    def deleteFront(self):
        print('deleteFront not implemented ')
    def clear(self):
        print('clear not implemented')
    def getRank(self, page):
        print('getRank not implemented')
    def size(self) :
        return self.T1.size( ) + self.T2.size()
    
    def getLeastFrequent(self):
        print('getLeastFrequent not implemented')
    def getLeastRecent(self):
        print('getLeastRecent not implemented')

    def __contains__(self, page) :
        if page in self.T1 or page in self.T2 :
            return True
        return False
    
    def add(self, page):
        t1 = self.T1.size()
        t2 = self.T2.size()
        b1 = self.B1.size()
        if t1 + t2 == self.N :
            print('Error adding. DT is full')
            
        if page in self.B1:
            
            if self.B2.size() > self.B1.size() :
                r = self.B2.size() / self.B1.size()
            else :
                r = 1
            self.P = min(self.P + r, self.N)
            
            assert self.B1.delete(page)
            assert self.T2.size()< self.N
            assert self.T2.add(page)
            
        elif page in self.B2:
            if self.B1.size() > self.B2.size() :
                r = self.B1.size() / self.B2.size()
            else :
                r = 1
            self.P = max(self.P - r, 0)
            
            assert self.B2.delete(page)
            assert self.T2.size()< self.N
            assert self.T2.add(page)
            
        else:
            if t1 + b1 == self.N:
                assert t1 < self.N, 't1 = %d' % t1
                assert b1 > 0 , 't1 = %d' % b1
                assert self.B1.deleteFront() is not None
            assert self.T1.add(page)
            
        assert page not in self.B1
        assert page not in self.B2
        assert page in self.T1 or page in self.T2
        assert not (page in self.T1 and page in self.T2)
        
        
        
        
        
    def delete(self, page):
        if page in self.T1:
            self.T1.delete(page)
        if page in self.T2:
            self.T2.delete(page)
    
    def replacePage(self, oldpage, newpage):
        self.delete(oldpage)
        self.add(newpage)
    
    def request(self,page) :
        t1 = self.T1.size()
        t2 = self.T2.size()
        b1 = self.B1.size()
        b2 = self.B2.size()
        
        assert t1+t2 <= self.N, 'Error: t1+t2 should not be bigger than self.N. t1+t2=%d+%d=%d' % (t1,t2,t1+t2)
        assert t1+b1 <= self.N, 'Error: t1+b1 should not be bigger than self.N. t1+b1=%d+%d=%d' % (t1,b1,t1+b1)
        assert t1+t2+b1+b2 <= 2*self.N, 'Error: t1+t2+b1+b2 should not be bigger than 2*self.N. t1+t2+b1+b2=%d+%d+%d+%d=%d' % (t1,t2,b1,b2,t1+t2+b1+b2)
        
        
        evited_page = None
        
        if page in self.T1  or page in self.T2:
            if page in self.T1 :
                assert self.T1.delete(page)
            if page in self.T2 :
                assert self.T2.delete(page)

            assert self.T2.add(page), 'failed adding to T2 at Case 1'

        elif page in self.B1 :
            if self.B2.size() > self.B1.size() :
                r = self.B2.size() / self.B1.size()
            else :
                r = 1
            self.P = min(self.P + r, self.N)
            assert self.B1.delete(page)
            evited_page = self.__replace(page, self.P)
            assert self.T2.add(page), 'failed adding to T2 at case B1'
        elif page in self.B2 :
            if self.B1.size() > self.B2.size() :
                r = self.B1.size() / self.B2.size()
            else :
                r = 1
            self.P = max(self.P - r, 0)
            assert self.B2.delete(page)
            evited_page = self.__replace(page, self.P)
            assert self.T2.add(page), 'failed adding to T2  at case B2'
        else :
            if t1 + b1 == self.N :
                if t1 < self.N :
                    assert self.B1.deleteFront() is not None, 'Error deleting front of B1'
                    evited_page = self.__replace(page, self.P)
                else :
                    evited_page = self.T1.deleteFront()
                    assert evited_page is not None, 'Error deleting front of T1'
            elif t1 + b1 < self.N :
                if t1 + t2 + b1 + b2 >= self.N :
                    if t1 + t2 + b1 + b2 == 2 * self.N :
                        assert self.B2.deleteFront() is not None,  'Error deleting front of B2'
                    evited_page = self.__replace(page, self.P)

            # Add page to the MRU position in T1
            assert page not in self.B1, 'Error. %d is not suppose to be in B1. debug %d %d' % (page,self.B1.inDisk(page), page in self.B1)
            assert self.T1.add(page), 'failed adding page to T1 at case 4'
        
        data = self.T1.get_data_as_set() | self.T2.get_data_as_set()
        for p in data:
            self.__checkpage(p)
        
        return evited_page
    
    
    def __checkpage(self, page):
        int1 = 1 if page in self.T1 else 0
        int2 = 1 if page in self.T2 else 0
        inb1 = 1 if page in self.B1 else 0
        inb2 = 1 if page in self.B2 else 0
        assert int1 + int2 + inb1 + inb2 == 1, "error: %d can only be in one list. count = %d %d %d %d = %d" % (page, int1, int2, inb1 , inb2,int1 + int2 + inb1 + inb2 ) 
        
        
    
    def __replace(self,x, P) :
        
        if self.T1.size() > 0 and (self.T1.size() > P or  (self.B1.inDisk(x) and self.T1.size() == int(P))):
            y = self.T1.deleteFront()
            assert y is not None, 'Error deleting front of T1 in replace (Case 1)'
            
            assert y not in self.T1, 'Error. %d is not suppose to be in T1' % y
            
            assert self.B1.add(y), 'failed adding page to B1 at replace 1(Case 1) %d' % y
            
            assert y not in self.T1 and y in self.B1, "Error moving from T1 to B1"
            
        else:
            y = self.T2.deleteFront()
            assert y is not None, 'Error deleting front of T2 in replace (Case 2)'
            assert self.B2.add(y), 'failed adding page to B2 at replace 1(Case 2)'
        return y

    
    def pageEvict(self, page):
        t1 = self.T1.size()
        t2 = self.T2.size()
        b1 = self.B1.size()
        b2 = self.B2.size()
        
        if t1 + t2 < self.N:
            return None
        
        evited_page = None
        if self.B1.inDisk(page) :
            if self.B2.size() > self.B1.size() :
                r = self.B2.size() / self.B1.size()
            else :
                r = 1
            tempP = min(self.P + r, self.N)
            evited_page = self.__replaceNoChange(page,tempP)
        elif self.B2.inDisk(page) :
            if self.B1.size() > self.B2.size() :
                r = self.B1.size() / self.B2.size()
            else :
                r = 1
            tempP = max(self.P - r, 0)
            evited_page = self.__replaceNoChange(page, tempP)
        else :
            tempP = self.P
            if t1 + b1 == self.N :
                if t1 < self.N :
                    evited_page = self.__replaceNoChange(page,tempP)
                else :
                    evited_page = self.T1.getIthPage(0)
            elif t1 + b1 < self.N :
                if t1 + t2 + b1 + b2 >= self.N :
                    evited_page = self.__replaceNoChange(page,tempP)
        
        return evited_page


    def __replaceNoChange(self,x, P) :
        if self.T1.size() > 0 and (self.T1.size() > P or  (self.B1.inDisk(x) and self.T1.size() == int(P))):
            return self.T1.getIthPage(0)
        else:
            return self.T2.getIthPage(0)
