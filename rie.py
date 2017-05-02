# -*- coding: utf-8 -*-
#/almac/ignacio/data/sts_all/split_dir/f_46081.splt^I0^Ibulb^Iis in^Iits path^I1^I2^I2^I4^I4^I7^I1.000^Ieach bulb is in its own path^IDT NN VBZ IN PRP$ JJ NN^Ibulb^Ibe in^Iits path
#/almac/ignacio/data/sts_all/split_dir/f_46081.splt^I0^Ibulb^Iis in^Iits own path^I1^I2^I2^I4^I4^I7^I1.000^Ieach bulb is in its own path^IDT NN VBZ IN PRP$ JJ NN^Ibulb^Ibe in^Iits own path
#/almac/ignacio/data/sts_all/split_dir/f_58672.splt^I0^IU.N.^Iregulate^Iarms trade^I0^I1^I2^I3^I4^I6^I1.000^IU.N. to regulate global arms trade^INNP TO VB JJ NNS NN^IU.N.^Iregulate^Iarm trade
#/almac/ignacio/data/sts_all/split_dir/f_73695.splt^I0^IIron Dome^Iis in^ICentral^I3^I5^I5^I6^I6^I7^I1.000^IIDF to deploy Iron Dome in Central Israel^INN TO VB NNP NNP IN NNP NNP^IIron Dome^Ibe in^ICentral
import argparse
import fasttext
from numpy import mean, median
from pdb import set_trace  as st

stoplist = 'it in is are been of the this those a these that then if thus with'.split()

class corpus_streamer(object):
    """ This Object streams the input raw text file row by row. The constructor
    allows for streaming a dictionary (object), strings (True), lists (by space
    or any character) and sublists of strings (position='a:b') or a substring
    from the list in a specific position (position=index).
    """
    def __init__(self, file_name, dictionary=None, strings=None,
                                                    spliter="", position=":"):
        self.file_name=file_name
        self.dictionary=dictionary
        self.strings=strings
        self.spliter=spliter
        self.position=position
    def __iter__(self):
        for line in open(self.file_name):
        # assume there's one document per line, tokens separated by whitespace
            if self.dictionary and not self.strings:
                yield self.dictionary.doc2bow(line.lower().split())
            elif not self.dictionary and self.strings:
                if self.spliter=="":
                    yield line.strip()
                if self.position==":":
                    yield line.strip().split(self.spliter)
                elif not isinstance(self.position, int) and len(self.position)>1:
                    i,f=map(int, self.position.split(":"))
                    yield line.strip().split(self.spliter)[i:f]
                elif isinstance(self.position, int):
                    yield line.strip().split(self.spliter)[self.position]


def dist_rank(phrases_list, we_model, ri_centroids, th=5):
    """ This function generates Regulatoy Interaction (RI) clusters. Given
    cluster centroids, there are two rankings. The former (vertical pathway)
    ranks all elements from each triplete category according to its cosine
    distance to each RI cluster centroid. The second ranking (horizontal
    pathway) ranks each element w.r.t the best RI cluster centroid.
    """
    #for phrase in phrases_list:

def set_compr(trip_dict, ops=["U","U","I"]):
    """Compress a set of tripletes by performing set operations inside a unique
    category, e.g. the union/intersection of the elements of 'NPa'.
    """
    triplet={"NPa": set(),
                "VP": set(),
                "NPb": set()
                }
    assert len(ops) == 3 # Exacly 3 operators must be provided.
# Probably set operations can change according to application (i.e. some operations
# favore RIe-GCe and other ones favore STS.)
    op={"U": set.union,
            "I": set.intersection,
            "D": set.difference,
            "X": set.symmetric_difference
            }
    for i in trip_dict:
        for l in trip_dict[i]:
            for j in trip_dict[i]:
                if i=="NPa":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(op[ops[0]](*[set(l),set(j)]))
                if i=="VP":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(op[ops[1]](*[set(l),set(j)]))
                if i=="NPb":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(op[ops[2]](*[set(l),set(j)]))
    return triplet

def avg_compr(trip_dict, get="avg"):
    """Produces the ategory VP/NP average length from of all triples given a
    sentence. Probably the general (noun) phrase average length is near to 5. In
    the case there are many phrases, I chose the nearest one to the average in
    length. A possible reference is: Temperley D. (2005) 'The Dependency
    Structure of Coordinate Phrases: A Corpus Approach'."""
    from operator import itemgetter as ig

    for t in trip_dict:
    #trip_dict[t]=(trip_dict[t], max(trip_dict[t],key=len))
        if get == "max":
            trip_dict[t]=max(trip_dict[t],key=len)
        elif get == "avg": # {'VP': [['activate']], 'NPa': [['ability']], 'NPb': [['fimb', 'expression']]}
            length=round(mean([len(f) for f in trip_dict[t]]))
            rank=sorted([(i, abs(len(f) - length)) for i,f in enumerate(trip_dict[t])],
                                                    key=lambda tup: tup[1])
            filt=[j[0] for j in rank if j[1]<=1]
            phrases_meet=ig(*filt)(trip_dict[t])
            st()
            trip_dict[t]=list(trip_dict[t])[i]
        elif get == "med":
            length=int(median([len(f) for f in trip_dict[t]]))
            i=sorted([(i, abs(len(f) - length)) for i,f in enumerate(trip_dict[t])],
                                                    key=lambda tup: tup[1])[0][0]
            trip_dict[t]=list(trip_dict[t])[i]
            #print i
            #print length
            #print trip_dict
    return trip_dict

def compressor(triplets, op="avg"):

    trip_dict={"NPa":0, "VP":1, "NPb":2}

    trip_dict={y:[list(set(s.split())
                    -(set(s.split())&set(stoplist)) )
                for s in set([x[trip_dict[y]]
                    for x in triplets])]
                        for y in trip_dict
              }
    if isinstance(op,list):
        yield set_compr(trip_dict, ops=op)
    else:
        yield avg_compr(trip_dict, get=op)

def vec2dict(vec_file, mt=True):
    from contextlib import closing as cl
    import shelve as shl
    from numpy import array
    
    word_vectors=corpus_streamer(vec_file, strings=True, spliter=" ")
    if not mt:
        with cl(shl.open(vec_file+".dict", writeback=True)) as f:
            for vector in word_vectors:
                f[vector[0]]=array([float(v) for v in vector[1:]])
    else:
        import threading
        import Queue
        import sys

        #def do_work(in_queue, out_queue):
        #    while True:

        #        vector=in_queue.get()
        #        with cl(shl.open(vec_file+".dict", writeback=True)) as f:

        #            f[vector[0]]=array([float(v) for v in vector[1:]])
        #        result = vector
        #        out_queue.put(result)
        #        in_queue.task_done()


        #work = Queue.Queue()
        #results = Queue.Queue()
        #total = 10

    # start for workers
        #for i in xrange(2):
        #    t = threading.Thread(target=do_work, args=(work, results))
        #    t.daemon = True
        #    t.start()

    # produce data

        #for v in word_vectors:
        #    work.put(v)

        #work.join()

    # get the results
        #for i in xrange(total):
            #print results.get()

            #sys.exit()

    def do_work(vector):
        with cl(shl.open(vec_file+".dict", writeback=True)) as f:
            f[vector[0]]=array([float(v) for v in vector[1:]])

    def worker():
        while True:
            vector = q.get()
            if vector is None:
                break
            do_work(vector)
            q.task_done()

    import queue

    num_worker_threads=3
    q = queue.Queue()
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for v in word_vectors:
        q.put(v)

# block until all tasks are done
    q.join()
# stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()
