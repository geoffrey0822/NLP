import os,sys,io
import numpy as np
import lmdb
import base64

output_path=sys.argv[2]
word_dict=[]
total_rec=0
irec=0
map_size=1024*1024*1024*2 # 2Gb
with io.open(sys.argv[1],'r',encoding='utf-8') as inputf:
    for line in inputf:
        total_rec+=1
    print 'there are %d records' %total_rec
    
with io.open(sys.argv[1],'r',encoding='utf-8') as inputf:
    with lmdb.open(output_path,map_size=map_size) as env:
        txn=env.begin(write=True)
        i=0
        for line in inputf:
            words=line.split(' ')
            for word in words:
                key=base64.b64encode(word.encode('utf-8'))
                txn.put(str(i),key,dupdata=False,overwrite=False)
                i+=1
                if i%1000==0:
                    txn.commit()
                    txn=env.begin(write=True)
                    #print '%d words are saved'%(i)
            irec+=1
            if irec%10000==0:
                print '%d/%d are saved'%(irec,total_rec)
        txn.commit()
    print 'there are %d words'%i
print 'finished'
        
    #with io.open(sys.argv[2],'w',encoding='utf-8') as outputf: