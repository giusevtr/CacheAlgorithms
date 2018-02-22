import numpy as np

NUM_REQUEST = 40000
UNIQUE_PAGES = 500
PHASE_SHIFTS = 200
RANDOMIZATION_RATE = 0.10
CACHE_SIZE = 50
PROB_USED = 0.95
DECAY_RATE = 0.99

HARD_PHASE_SHIFT = NUM_REQUEST/2
# LRU_PROB = 0.9

Q = list()
F = {}
time = 0

## Choose page using a uniform distribution
def Random():
    return np.random.randint(0, UNIQUE_PAGES)

## Choose page using LRU distribution
def LRU():
    
    n = min(CACHE_SIZE, len(F))
    lamb = -np.log(1-PROB_USED) / n
    used = {}
    x = 1
    
    qlen = len(Q)
    for i,pg in enumerate(Q[::-1]) :
        if pg in used :
            del Q[qlen - i - 1]
        else :
            prob = lamb*np.exp(-lamb * x)
            if np.random.rand() < prob :
                return pg
            x += 1
        used[pg] = 1
        
    return np.random.randint(0, UNIQUE_PAGES)

## Choose page using LFU distribution
def LFU():
    n = min(CACHE_SIZE, len(F))
    lamb = -np.log(1-PROB_USED) / n
    i = 0
    L = []
    for key in F :
        if i >= n :
            break
        i += 1
        L.append((-F[key], key))
    
    L.sort()
    
    for x,pg in enumerate(L):
        prob = lamb*np.exp(-lamb * x)
        if np.random.rand() < prob :
            return pg[1]
        
    
    return np.random.randint(0, UNIQUE_PAGES)

def update(page):
    Q.append(page)
    if page not in F :
        F[page] = 0
    F[page] += 1
    
if __name__ == "__main__" :
    phase = 1
    for i in range(0, NUM_REQUEST) :
        if i == HARD_PHASE_SHIFT :
            phase = 1 - phase
#         if i % PHASE_SHIFTS == 0 :
#             phase = 0 if np.random.rand() < LRU_PROB else 1

        ## With probability RANDOMIZATION_RATE choose a page from a uniform distribution
        randomize = True if time == 0 or  np.random.rand() < RANDOMIZATION_RATE else False

        if randomize :
            q = Random()
        else :
            if phase == 0 :
                q = LRU()
            if phase == 1 :
                q = LFU()        
        update(q)        
        print('%d' % q)
        
        time += 1
        
        