import sys



class page_replacement_algorithm :
    def __init__(self, N, visualization = False):
        pass
    def request(self,page) :
        pass
    def page_color(self, p ) :
        return 0 ## color white
    def get_list_labels(self) :
        return []
    def get_data(self):
        return []
    def page_label(self,page):
        return str(page)
    def get_N(self) :
        raise('Need to implement this method')
    
    def visualize(self, plt):
        pass
    
    def test_algorithm(self,pages,  partition_size = 10) :
        hits = 0
        last_percent = -1
        num_pages = len(pages)

        N = self.get_N()

#         part_hits = 0
#         part_count = 0

        partition_hit_rate = []
        hit_sum = []

        # print ''
        for i,p in enumerate(pages) :
            if not self.request(p) and i > N:
                hits += 1
#                 part_hits += 1
#             if i > N :
#                 part_count += 1

            hit_sum.append(hits)

#             if part_count == partition_size or i+1 == num_pages:
#                 partition_hit_rate.append(round(1.0 * part_hits / part_count,2))
#                 part_hits = 0
#                 part_count = 0

            ## Progres
            percent = int ((100.0 * (i+1) / num_pages))
            if percent != last_percent and percent % 10 == 0 :
                # print percent
                bars = int(percent / 10)
                sys.stdout.write('|')
                for i in range(bars) :
                    sys.stdout.write('=')
                for i in range(10 - bars ) :
                    sys.stdout.write(' ')
                sys.stdout.write('|\r')
                sys.stdout.flush()
                last_percent = percent

        for i in range(15 ) :
            sys.stdout.write(' ')
        sys.stdout.write('\r')

        return hits,partition_hit_rate,hit_sum
