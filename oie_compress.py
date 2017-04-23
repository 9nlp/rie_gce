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

parser = argparse.ArgumentParser()
parser.add_argument("--oie", help="Input file containing openIE triplets to be compresses.", required=True)
parser.add_argument("--o", help="Output file for compressed openIE triplets.")
args = parser.parse_args()

with open(args.oie) as f:
  triplets=map(str.strip().split("\t")[1:], f.readlines())

if len(triplets) < 3:
    print "No triplets in file %s" % args.oie
    exit()

for c in xrange(3):
    [row[c] for row in triplets]
