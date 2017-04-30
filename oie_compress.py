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
    """ This Object streams the input raw text file row by row.
    """
    def __init__(self, file_name, dictionary=None, strings=None, spliter="", position=":"):
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

def set_compr(trip_dict):
    triplet={"NPa":set(), "VP":set(), "NPb":set()}
# Probably set operations can change according to application (i.e. some operations
# favore RIe-GCe and other ones favore STS.)
    for i in trip_dict:
        for l in trip_dict[i]:
            for j in trip_dict[i]:
                if i=="NPa":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(set(l)|set(j))
                if i=="VP":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(set(l)|set(j))
                if i=="NPb":
                    if len(trip_dict[i]) == 1:
                        triplet[i].update(set(l))
                    elif j!=l:
                        triplet[i].update(set(l)&set(j))
    return triplet

def avg_compr(trip_dict, get="avg"):
# I decided to use the VP/NP average length of all triples for each triple. 
# Probably the general phrase average length is near to 5. In the case there
# are many phrases, I chose the nearest one to the average in length.
# A possible reference: Temperley D. (2005) "The Dependency Structure of 
# Coordinate Phrases: A Corpus Approach"

    for t in trip_dict: 
    #trip_dict[t]=(trip_dict[t], max(trip_dict[t],key=len))
        if get == "max":
            trip_dict[t]=max(trip_dict[t],key=len)
        elif get == "avg": # {'VP': [['activate']], 'NPa': [['ability']], 'NPb': [['fimb', 'expression']]}
            length=round(mean([len(f) for f in trip_dict[t]]))
            i=sorted([(i, abs(len(f) - length)) for i,f in enumerate(trip_dict[t])], key=lambda tup: tup[1])[0][0]
            trip_dict[t]=list(trip_dict[t])[i]
        elif get == "med":
            length=int(median([len(f) for f in trip_dict[t]]))
            i=sorted([(i, abs(len(f) - length)) for i,f in enumerate(trip_dict[t])], key=lambda tup: tup[1])[0][0]
            trip_dict[t]=list(trip_dict[t])[i]
            print i
            print length
            print trip_dict
    return trip_dict

def compressor(triplets, op="avg"):

    trip_dict={"NPa":0, "VP":1, "NPb":2}

    trip_dict={y:[list(set(s.split())
                    -(set(s.split())&set(stoplist)) ) 
                for s in set([x[trip_dict[y]] 
                    for x in triplets])] 
                        for y in trip_dict
              }

    if op=="set":
        yield set_compr(trip_dict)
    elif op=="avg":
        yield avg_compr(trip_dict, get="med")

# __main__()

parser = argparse.ArgumentParser()
parser.add_argument("--oie", help="Input file containing openIE triplets of a sentence.", default=None)
parser.add_argument("--oies", help="Input file containing openIE triplets of all sentences.", default=None)
parser.add_argument("--op", help="Operation performed among keys of a openIE triplets set op='set','avg'.", default="avg")
parser.add_argument("--o", help="Output file for compressed openIE triplet(s).", default=None)
args = parser.parse_args()

assert args.oie or args.oies # At least one input file must be provided.
# The stop list can depend on the application. i.e. Probably for RIe-GCe we 
# would not need for trivial relational verbs, causing noise to vector sums,
# but for semantic similarity, probably these verbs are a bit necessary.
#stoplist = 'for a of the and to in is are were been have had has'.split()
if args.oie:
    with open(args.oie) as f:
        triplets=[line.strip().split("\t")[1:] for line in f.readlines()]
    if len(triplets[0]) < 3:
        print "No triplets in file %s" % args.oie
        exit()

elif args.oies:
    files=corpus_streamer(args.oies, strings=True, spliter="\t")
    triplets={}
    for file in files:
        if file[0].split("/")[-1] in triplets:
            triplets[file[0].split("/")[-1]].append(file[-3:])
        else:
            triplets[file[0].split("/")[-1]]=list()
            triplets[file[0].split("/")[-1]].append(file[-3:])
# metrez il à une function:
triplets={triplet: compressor(triplets[triplet], op=args.op) for triplet in triplets}

if not args.o:
    for t in triplets:
        print "%s:\t%s" % (t, [tr for tr in triplets[t]])
else:
    with open(args.o, "w") as f:
        for t in triplets:
            f.write("%s:\t%s\n" % (t, [tr for tr in triplets[t]]))

# 1.0	much	be paid on	insurance claim
# 1.0	much	is	paid
# 1.0	much	is	paid on insurance claim
# 1.0	much	be	paid
# -----------------------------------------------------
# 1.0	channel	joining	two bodies
# 1.0	channel	joining	two larger bodies of water
# 1.0	channel	joining	two larger bodies
# 1.0	channel	joining	two bodies of water
# 1.0	narrow channel	joining	two bodies of water
# 1.0	narrow channel	joining	two larger bodies
# 1.0	narrow channel	joining	two larger bodies of water
# 1.0	narrow channel	joining	two bodies
