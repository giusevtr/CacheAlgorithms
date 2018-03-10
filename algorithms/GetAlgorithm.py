'''
Created on Feb 17, 2018

@author: giuseppe
'''
from algorithms.LRU import LRU
from algorithms.MRU import MRU
from algorithms.LFU import LFU
from algorithms.LFU_DECAY2 import LFU_DECAY2 
from algorithms.LFU_DECAY import LFU_DECAY
from algorithms.ARC import ARC
from algorithms.MARKING import MARKING
from algorithms.WALK_MARKING_SLOW import WALK_MARKING_SLOW
from algorithms.WALK_MARKING import WALK_MARKING
from algorithms.PAGERANK_MARKING_SLOW import PAGERANK_MARKING_SLOW
from algorithms.PAGERANK_MARKING_FAST import PAGERANK_MARKING_FAST
from algorithms.FAR import FAR
from algorithms.LaCReME_LFU_ARC import LaCReME_LFU_ARC
from algorithms.RANDOM import RANDOM
from algorithms.BANDIT import BANDIT
from algorithms.BANDIT2 import BANDIT2
from algorithms.BANDIT3 import BANDIT3
from algorithms.LaCReME import LaCReME
from algorithms.LaCReME_simple import LaCReME_simple
from algorithms.LaCrema2 import LaCrema2
from algorithms.LaCReME_context1 import LaCReME_context1
from algorithms.LaCReME_LFU_ARC import LaCReME_LFU_ARC
from algorithms.LaCReME_T1T2 import LaCReME_T1T2
from algorithms.LaCReME_v2 import LaCReME_v2
from algorithms.LaCReME_v3 import LaCReME_v3
from algorithms.LOMP import LOMP
from algorithms.OLCR import OLCR
from algorithms.OLCR_RAND import OLCR_RAND



from algorithms.BANDIT_WITH_ARC import BANDIT_WITH_ARC

def GetAlgorithm(cache_size,name, visualization = False):
    lower_name = name.lower()
    if lower_name == 'arc' :
        return ARC(cache_size)
    elif lower_name == 'marking' :
        return  MARKING(cache_size)
    elif lower_name == 'lru' :
        return LRU(cache_size)
    elif lower_name == 'mru' :
        return MRU(cache_size)
    elif lower_name == 'lfu' :
        return LFU(cache_size)
    elif lower_name == 'lfu_decay2' :
        return LFU_DECAY2(cache_size)
    elif lower_name == 'lfu_decay' :
        return LFU_DECAY(cache_size)
    elif lower_name == 'lfu1' :
        return LFU_DECAY(cache_size,decay=1)
    elif lower_name == 'lfu2' :
        return LFU_DECAY(cache_size,decay=0.9)
    elif lower_name == 'pagerank_fast' :
        return PAGERANK_MARKING_FAST(cache_size)
    elif lower_name == 'pagerank_slow' :
        return PAGERANK_MARKING_SLOW(cache_size)
    elif lower_name == 'walk' :
        return WALK_MARKING(cache_size)
    elif lower_name == 'walkslow' :
        return WALK_MARKING_SLOW(cache_size)
    elif lower_name == 'far' :
        return FAR(cache_size)
    elif lower_name == 'random' :
        return RANDOM(cache_size)
    elif lower_name == 'bandit' :
        return BANDIT(cache_size)
    elif lower_name == 'bandit2' :
        return BANDIT2(cache_size)
    elif lower_name == 'bandit3' :
        return BANDIT3(cache_size)
    elif lower_name == 'lacreme' :
        return LaCReME(cache_size,visualization)
    elif lower_name == 'lacrema2' :
        return LaCrema2(cache_size)
    elif lower_name == 'lacreme_simple' :
        return LaCReME_simple(cache_size)
    elif lower_name == 'lacreme_lru_arc' :
        return LaCReME_LFU_ARC(cache_size)
    elif lower_name == 'lacreme_context1' :
        return LaCReME_context1(cache_size)
    elif lower_name == 'lacreme_lfu_arc' :
        return LaCReME_LFU_ARC(cache_size)
    elif lower_name == 'lacreme_t1t2' :
        return LaCReME_T1T2(cache_size)
    elif lower_name == 'lacreme_v3' :
        return LaCReME_v3(cache_size)
    elif lower_name == 'lomp' :
        return LOMP(cache_size)
    elif lower_name == 'bandit_with_arc' :
        return BANDIT_WITH_ARC(cache_size)   
    elif lower_name == 'olcr' :
        return OLCR(cache_size)   
    elif lower_name == 'olcr_rand' :
        return OLCR_RAND(cache_size)   
    
    return None       


