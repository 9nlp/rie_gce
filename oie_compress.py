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

import argparse
import fasttext
from numpy import mean, median
from pdb import set_trace  as st

parser = argparse.ArgumentParser()
parser.add_argument("--oie", help="Input file containing openIE triplets to be compresses.", required=True)
parser.add_argument("--o", help="Output file for compressed openIE triplets.")
args = parser.parse_args()

#get="avg" 
#get="max" 
get="med"
#stoplist = 'for a of the and to in is are were been have had has'.split()
stoplist = 'is are been'.split()

with open(args.oie) as f:
    triplets=[line.strip().split("\t")[1:] for line in f.readlines()]

if len(triplets[0]) < 3:
    print "No triplets in file %s" % args.oie
    exit()

trip_dict={}

trip_dict["NPa"]=set([row[0] for row in triplets if row[0] not in stoplist])
trip_dict["VP"]=set([row[1] for row in triplets if row[1] not in stoplist])
trip_dict["NPb"]=set([row[2] for row in triplets if row[2] not in stoplist])

# I decided to use the VP/NP average length of all triples for each triple. 
# Probably the general phrase average length is near to 5. In the case there
# are many phrases, I chose the nearest one to the average in length.
# A possible reference: Temperley D. (2005) "The Dependency Structure of 
# Coordinate Phrases: A Corpus Approach"

for t in trip_dict: 
    #trip_dict[t]=(trip_dict[t], max(trip_dict[t],key=len))
    if get == "max":
        trip_dict[t]=max(trip_dict[t],key=len)
    elif get == "avg":
        length=round(mean([len(f.split()) for f in trip_dict[t]]))
        i=sorted([(i, abs(len(f.split()) - length)) for i,f in enumerate(trip_dict[t])], key=lambda tup: tup[1])[0][0]
        trip_dict[t]=list(trip_dict[t])[i]
    elif get == "med":
        length=round(median([len(f.split()) for f in trip_dict[t]]))
        i=sorted([(i, abs(len(f.split()) - length)) for i,f in enumerate(trip_dict[t])], key=lambda tup: tup[1])[0][0]
        trip_dict[t]=list(trip_dict[t])[i]

print trip_dict
