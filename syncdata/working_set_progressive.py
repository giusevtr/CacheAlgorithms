import numpy as np
from audioop import add

CACHE_SIZE = 50
PHASE_SIZE = 1000
NUM_PHASES = 10
UNIVERSE_SIZE = 500
WORKING_SET_SIZE = 100
WS_CHANGE_STEP = 3
CHANGE_PER_PHASE = 80

if __name__ == "__main__" :
    current_group = None
    
    other = np.arange(0,UNIVERSE_SIZE, dtype=np.int32)
    workingSet = np.array([], dtype=np.int32)
    
    
    eps = 0.2
    for i in range(0, NUM_PHASES) :
     
        
        currently_replaced = 0
        for _ in range(0, PHASE_SIZE) :
        
            if currently_replaced < CHANGE_PER_PHASE:
                for x in range(0, WS_CHANGE_STEP):
                    other_idx = np.random.randint(0, len(other))
                    other_page = other[other_idx]
                    other = np.delete(other, other_idx)
                    
                    if len(workingSet) >= WORKING_SET_SIZE:
                        ws_idx = np.random.randint(0, len(workingSet))
                        ws_page = workingSet[ws_idx]
                        workingSet = np.delete(workingSet, ws_idx)
                        other = np.append(other, ws_page)
                    
                    workingSet = np.append(workingSet, other_page)
                    currently_replaced += 1
                
            if np.random.rand() < 1-eps :
                q = workingSet[np.random.randint(0,len(workingSet))]
            else:
                q = other[np.random.randint(0,len(other))]
            print int(q)
    
        ## Create a vertical line
        print -1
        