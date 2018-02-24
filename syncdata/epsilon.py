import numpy as np

NUM_REQUEST = 40000
UNIQUE_PAGES = 500
PHASE_SHIFTS = 200
RANDOMIZATION_RATE = 0.25
CACHE_SIZE = 50
PROB_USED = 0.8
DECAY_RATE = 1

HARD_PHASE_SHIFT = NUM_REQUEST/2
# LRU_PROB = 0.9

Q = list()
F = {}
R = {}
time = 0

## Choose page using a uniform distribution
def Random():
    return np.random.randint(0, UNIQUE_PAGES)

## Choose page using LRU distribution
def LRU():
    global Q
    global F
    n = min(CACHE_SIZE, len(F))
    L = []
    seen = {}
    for i,pg in enumerate(Q[::-1]) :
        if len(seen) >= n :
            break
        if pg in seen:
            continue
        L.append((F[pg],pg))
        seen[pg] = 1
    L.sort()
    minfreqpages = 0
    while minfreqpages < len(L) and L[0][0] == L[minfreqpages][0] :
        minfreqpages +=1
    return L[np.random.randint(0,minfreqpages)][1]
#     return L[np.random.randint(0, n)][1]

## Choose page using LFU distribution
def LFU():
    global F
    global R
    n = min(CACHE_SIZE, len(F))
    L = []
    for key in F :
        L.append((-F[key], key))
    L.sort()
    temp =[]
    for i,pg in enumerate(L):
        if i >= n :
            break
        page = pg[1]
        temp.append((R[page],page))
    
    return min(temp)[1]
#     return temp[np.random.randint(0, n)][1]

def update(page):
    global time
    global Q
    global R
    global F
    Q.append(page)
    if page not in F :
        F[page] = 0
    F[page] += 1
    R[page] = time
    time += 1
    
if __name__ == "__main__" :
    phase = 1
    epsilon = 0.25
    
    for i in range(0, NUM_REQUEST) :
        if i == HARD_PHASE_SHIFT :
            phase = 1 - phase

        ## With probability RANDOMIZATION_RATE choose a page from a uniform distribution
        randomize = True if time < CACHE_SIZE or  np.random.rand() < epsilon else False

        if randomize :
            q = Random()
        else :
            if phase == 0 :
                q = LRU()
            if phase == 1 :
                q = LFU()        
        update(q)        
        print(q)
        
        