import os,sys,leveldb

db=leveldb.LevelDB(sys.argv[1])
max=0
count=0
if len(sys.argv)>2:
    max=int(sys.argv[2])
for key,value in db.RangeIter():
    print value
    count+=1
    if max>0 and count>=max:
        break
    
print 'finish'