import lmdb
import os, sys

nrec=0
with lmdb.open(sys.argv[1]) as inputENV:
    txn=inputENV.begin()
    for key, value in txn.cursor():
        nrec+=1
    txn=inputENV.begin(write=True)
    for i in range(nrec):
        val=txn.get(str(i))
        for j in range(i,nrec):
            if i==j:
                continue
            cval=txn.get(str(j))
            if cval==val:
                txn.delete(str(j))
        txn.commit()
        txn=inputENV.begin(write=True)
    #txn=inputENV.begin(write=True)
print 'finished'