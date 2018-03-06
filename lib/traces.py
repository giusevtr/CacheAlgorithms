import numpy as np
import sys
import subprocess

class Trace:

    def __init__(self):
        self.traces = []
        self.G = {}
        # self.node_id = {}
        self.node_set = set()
        self.idMap = {}
    def get_request(self):
        # r = []
        # for T in self.traces :
        #
        #     node_name = int(T['name'])
        #     size = T['size']
        #
        #     for i in range(int(size / self.page_size)) :
        #         r.append(self.get_node_id(node_name))
        #         node_name += self.page_size


        return self.traces

    # def get_node_name(self, node_id):
    #     return node_name[node_id]
    #
    # def get_node_id(self, node_name) :
    #     self.__map_node(node_name)
    #     return self.node_id[node_name]
    
    def getId(self, node):
        if node not in self.idMap :
            i = len(self.idMap)
            self.idMap[node] = i
        return self.idMap[node]
    
    def read(self, file_name) :
        f = open(file_name, 'r')
        # self.traces.clear()

        del self.traces[:]

        if file_name.endswith('.blkparse') :
            for line in f :
                try :
                    row = line.split(' ')
                    node_name = int(row[3])
                    self.traces.append(node_name)
                    self.node_set.add(node_name)
                    # print(node_name)
                    # for i in range(int(size / self.page_size)) :
                    #    self.traces.append({'name' : node_name , 'id' : self.get_node_id(node_name), 'time' : time_stamp})
                    #    node_name += self.page_size
                except :
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print('Error')
                    print(exc_type, exc_value, exc_traceback)

        elif file_name.endswith('.spc') :
            temp = []
            page_size = 1e15

            for line in f :
                try :
                    row = line.split(',')
                    node_name = int(row[1])
                    size = int(row[2])
                    time_stamp = float(row[4])
                    if size == 0 :
                        continue
                    temp.append({'name' : row[1] , 'size' : size, 'time' : time_stamp})
                    page_size = min(page_size, size)
                    # print(node_name)
                    # for i in range(int(size / self.page_size)) :
                    #    self.traces.append({'name' : node_name , 'id' : self.get_node_id(node_name), 'time' : time_stamp})
                    #    node_name += self.page_size
                    self.traces.append(node_name)
                    self.node_set.add(node_name)
                except :
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print('Error')
                    print(exc_type, exc_value, exc_traceback)
            # print("=====================")

            for T in temp:
                node_name = int(T['name'])
                size = T['size']
                for _ in range(int(size / page_size)) :
                    j = self.getId(node_name)
                    self.traces.append(j)
                    self.node_set.add(j)
                    node_name += page_size
        elif file_name.endswith('.txt') :
            for line in f :
                x = int(line)
                self.traces.append(x)
                self.node_set.add(x)
            
    def number_of_request(self):
        return len(self.traces)

    def unique_pages(self):
        return len(self.node_set)

    # def get_access_graph(self) :
        return self.__create_access_graph()

if __name__ == "__main__" :

    t = Trace()

    t.read('/home/giuseppe/cache_database/Financial1.spc')
