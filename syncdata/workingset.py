import numpy as np
from audioop import add

CACHE_SIZE = 50
PHASE_SIZE = 500
NUM_PHASES = 5
UNIVERSE_SIZE = 500
WORKING_SET_SIZE = 100
WS_DELTA = 0.5

if __name__ == "__main__" :
    current_group = None
    
    other = np.arange(0,UNIVERSE_SIZE, dtype=np.int32)
    workingSet = np.array([], dtype=np.int32)
    
    eps = 0.2
    for i in range(0, NUM_PHASES) :
        
        
        n = len(workingSet)
        m = len(other)
        
        
        rem_ind = np.random.rand(n)
        add_ind = np.random.rand(m) 
        
        ## Remove a proportion WS_DELTA from the workingSet
        rand = np.random.rand(len(workingSet))
        ws_removed = workingSet[rand <= WS_DELTA] if len(workingSet) > 0 else np.array([])
        workingSet = workingSet[rand > WS_DELTA]
        
        
        ## Remove from other
        rand = np.random.rand(len(other)) 
        other_del = 1.0*(WORKING_SET_SIZE - len(workingSet)) / m
        o_removed = other[rand <= other_del]
        other = other[rand>other_del]

        ## Add pages
        workingSet = np.append(workingSet, o_removed)
        other = np.append(other, ws_removed)
        
        ## Create a vertical line
        print -1
        
        n = len(workingSet)
        m = len(other)
        
        for _ in range(0, PHASE_SIZE) :
        
            if np.random.rand() < 1-eps :
                q = workingSet[np.random.randint(0,n)]
            else:
                q = other[np.random.randint(0,m)]
            print int(q)
    
#         print current_group
        
        