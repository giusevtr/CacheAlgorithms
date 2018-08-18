'''
Created on Feb 17, 2018
@author: giuseppe
'''

from algorithms.LRU import LRU
from algorithms.MRU import MRU
from algorithms.LFU import LFU
from algorithms.ARC import ARC
from algorithms.MARKING import MARKING
from algorithms.FAR import FAR
from algorithms.RANDOM import RANDOM
from algorithms.LeCaR import LeCaR
from algorithms.LeCaR2 import LeCaR2
from algorithms.LeCaR3 import LeCaR3
<<<<<<< HEAD
from algorithms.LeCaR8 import LeCaR8
=======
from algorithms.LeCaR4 import LeCaR4
from algorithms.LeCaR5 import LeCaR5

>>>>>>> fc934d47084bff1e69fbc5990c40840758d1b967
from algorithms.LeCaR_clock import LeCaR_clock
from algorithms.LeCaR_fixed import LeCaR_fixed


# from algorithms.OLCR import OLCR



def GetAlgorithm(name):
    lower_name = name.lower()
    if lower_name == 'arc' :
        return ARC
    elif lower_name == 'marking' :
        return  MARKING
    elif lower_name == 'lru' :
        return LRU
    elif lower_name == 'mru' :
        return MRU
    elif lower_name == 'lfu' :
        return LFU
    elif lower_name == 'far' :
        return FAR
    elif lower_name == 'random' :
        return RANDOM
    elif lower_name == 'lecar' :
<<<<<<< HEAD
        return LeCaR  
    elif lower_name == 'lecar_clock' :
        return LeCaR_clock
    elif lower_name == 'lecar2' :
        return LeCaR2 
    elif lower_name == 'lecar3' :
        return LeCaR3
    elif lower_name == 'lecar8' :
        return LeCaR8
    
    return None       
=======
        return LeCaR
    elif lower_name == 'lecar_clock' :
        return LeCaR_clock
    elif lower_name == 'lecar2' :
        return LeCaR2
    elif lower_name  == 'lecar3' :
        return LeCaR3
    elif lower_name  == 'lecar4' :
        return LeCaR4
    elif lower_name == 'lecar_fixed' :
        return LeCaR_fixed
    elif lower_name == 'lecar5' :
        return LeCaR5



    return None
>>>>>>> fc934d47084bff1e69fbc5990c40840758d1b967


