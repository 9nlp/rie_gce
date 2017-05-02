from rie import *

# __main__()

parser = argparse.ArgumentParser()
parser.add_argument("--oie", help="""Input file containing openIE triplets of a
                                        sentence.""", default=None)
parser.add_argument("--oies", help="""Input file containing openIE triplets of
                                        all sentences.""", default=None)
parser.add_argument("--op", help="""Operation performed among keys of a openIE
                        triplets set op='U,U,I','avg', 'med'.""", default="med")
parser.add_argument("--o", help="Output file for compressed openIE triplet(s).",
                                                                default=None)
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
if len(args.op) > 3:
    if "," in args.op:
        op=args.op.split(",")
        if not isinstance(op, list) or len(op)!=3:
            print "Malformed operator option."
            exit()
else:
    op=args.op

triplets={triplet: compressor(triplets[triplet], op=op) for triplet in triplets}

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
