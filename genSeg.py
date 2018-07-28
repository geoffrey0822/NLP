import os,sys,io
import numpy as np
import jieba
import pickle

output_path=sys.argv[2]
with io.open(sys.argv[1],'r',encoding='utf-8') as txtf:
    with io.open(output_path,'w',encoding='utf-8') as outputf:
        i=0
        for line in txtf:
            words=' '.join(list(jieba.cut(line,cut_all=False)))
            outputf.write(words)
            i+=1
            if i%10000==0:
                print '%d data are processed'%i
        
print 'finished'