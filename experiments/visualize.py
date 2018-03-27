'''
Created on Mar 13, 2018

@author: giuseppe
'''
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt


def slidingWindow(data, ws):
    cumsum = np.cumsum(data)
    temp = np.append(np.zeros(ws), cumsum[:-ws])
    return (cumsum-temp) / ws
    
        
INPUT_CONFIG_FILE = 'config/input_data_location.txt'
OUTPUT_CONFIG_FILE = 'config/output_data_location.txt'

if os.path.isfile(OUTPUT_CONFIG_FILE) :
    f = open(OUTPUT_CONFIG_FILE, 'r')
    OUTPUT_FOLDER = f.readline().rstrip('\n\r')
else:
    print('No output file found! No csv file will be generated. Create file config/output_data_location.txt. to get the output data')
    OUTPUT_FOLDER = None
    
    
# inputfile = sys.argv[1]
# data = np.load(OUTPUT_FOLDER+inputfile)


# filename = 'madmax-110108-112108.3.blkparse_0.5%%'
# filename = '500_10000_LFU_ARCx4Result.txt_500'
filename = '500_10000_LFU_ARCx4Result.txt_500'
filename = 'ws_75x5.txt_50'

if len(sys.argv) > 1:
    filename = sys.argv[1]

print filename

madmax_pollution =    OUTPUT_FOLDER+'%s_pollution_'+filename+'.npy'
madmax_weights =    OUTPUT_FOLDER+'%s_weights_'+filename+'.npy'  
madmax_performance =    OUTPUT_FOLDER+'%s_hit_rate_'+filename+'.npy' 

lru_pollution = np.load(madmax_pollution % 'LRU')
lfu_pollution = np.load(madmax_pollution % 'LFU')
arc_pollution = np.load(madmax_pollution % 'ARC')
LeCaR_pollution = np.load(madmax_pollution % 'LeCaR')

LeCaR_weights = np.load(madmax_weights % 'LeCaR')

lru_performance = np.load(madmax_performance % 'LRU')
lfu_performance = np.load(madmax_performance % 'LFU')
arc_performance = np.load(madmax_performance % 'ARC')
LeCaR_performance = np.load(madmax_performance % 'LeCaR')



fig = plt.figure()
fig.subplots_adjust(hspace=.25)

# plt.ylim(-1,101)


#########################
## Pollution
#########################
ax = plt.subplot(3,1,1)
ax.set_title('Hoarding')
ax.set_ylim(-1,101)
ax.set_xlim(min(lru_pollution[:,0]),max(lru_pollution[:,0]))

ax.set_xticklabels([])
windowsize = 50
l1, = plt.plot(lru_pollution[:,0], slidingWindow(lru_pollution[:,1],windowsize), label='LRU', c='y', linewidth=2)
l2, = plt.plot(lfu_pollution[:,0], slidingWindow(lfu_pollution[:,1],windowsize) ,label='LFU', c='b', linewidth=2)
l3, = plt.plot(arc_pollution[:,0], slidingWindow(arc_pollution[:,1],windowsize) , label='ARC', c='r', linewidth=2)
l4, = plt.plot(LeCaR_pollution[:,0], slidingWindow(LeCaR_pollution[:,1],windowsize) , label='LeCaR', c='k', linewidth=2)
# plt.xlabel('Requests')

plt.ylabel('Hoarding Rate (%)')
plt.legend(handles=[l1,l2,l3,l4],fancybox=True, framealpha=0.5,fontsize=8,loc='center left', bbox_to_anchor=(1, 0.5))



#########################
## Weights
#########################
ax = plt.subplot(3,1,2)
ax.set_title('Weights')
ax.set_ylim(-0.01,1.01)
ax.set_xlim(min(LeCaR_weights[:,0]),max(LeCaR_weights[:,0]))

ax.set_xticklabels([])

# l3, = plt.plot(arc_weights[:,0], arc_weights[:,1] , label='ARC', c='r', linewidth=2)
l1, = plt.plot(LeCaR_weights[:,0], LeCaR_weights[:,1] , label='LRU_w', c='y', linewidth=2)
l2, = plt.plot(LeCaR_weights[:,0], LeCaR_weights[:,2] , label='LFU_w', c='b', linewidth=1)
# plt.xlabel('Requests')
plt.ylabel('Weight')
plt.legend(handles=[l1,l2],fancybox=True, framealpha=0.5,fontsize=8,loc='center left', bbox_to_anchor=(1, 0.5))


#########################
## Performance
#########################
ax = plt.subplot(3,1,3)
ax.set_title('Performance')
ax.set_ylim(-0.01,1.01)
ax.set_xlim(min(lru_performance[:,0]),max(lru_performance[:,0]))

l1, = plt.plot(lru_performance[:,0], lru_performance[:,1], label='LRU', c='y', linewidth=4)
l2, = plt.plot(lfu_performance[:,0], lfu_performance[:,1] ,label='LFU', c='b', linewidth=3)
l3, = plt.plot(arc_performance[:,0], arc_performance[:,1] , label='ARC', c='r', linewidth=2)
l4, = plt.plot(LeCaR_performance[:,0], LeCaR_performance[:,1] , label='LeCaR', c='k', linewidth=1)

plt.xlabel('Requests')
plt.ylabel('Hit rate (%)')
plt.legend(handles=[l1,l2,l3,l4],fancybox=True, framealpha=0.5,fontsize=8,loc='center left', bbox_to_anchor=(1, 0.5))
# plt.legend(handles=[l1,l2,l3,l4],fancybox=True, framealpha=0.5,fontsize=8)


if OUTPUT_FOLDER is not None:
    outputpath = '%s%s.png' % (OUTPUT_FOLDER,filename)
    plt.savefig(outputpath)
    print('Saving graph: ',outputpath)
# plt.show()






