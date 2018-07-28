import os,sys,leveldb

with open(sys.argv[1],'r') as f:
    db=leveldb.LevelDB(sys.argv[2])
    count=0
    print 'Converting CSV...',
    for ln in f:
        line=ln.rstrip('\n')
        #print line
        fields=line.split(',')
        db.Put(fields[0],fields[1])
        count+=1
        if count%10000==0:
            print '\rConverting...%d processed'%count,
    print 'finish'