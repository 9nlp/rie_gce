from pdb import set_trace as st
class vector_stream(object):
    def __init__(self, fpath):
        self.fpath = fpath
        self.fh = None

    def __enter__(self):
        self.fh = open(self.fpath)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fh.close()

    def __getitem__(self, item):
    #def __seek__(self, item):
        self.fh.seek(0)
        for line in self.fh:
            if line.startswith(item+" "):
                #return [float(number) for number in line[:-1].split(' ')[1:]]
                return [float(number) for number in line.strip().split(' ')[1:]]


#wl="thank you very much for your support".split()
#from pdb import set_trace as st
#with vector_stream(fpath="/home/iarroyof/data/glove/glove.6B.50d.txt") as word:
#    for w in wl:
#        print word[w]

#dic=vector_stream(fpath="/home/iarroyof/data/glove/glove.6B.50d.txt")
#st()
#for w in wl:
#    print dic.__getitem__(w)
