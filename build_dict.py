import jieba
import os,sys
import numpy
import xml.etree.ElementTree as ET
from gensim.corpora import WikiCorpus

dat_file=sys.argv[1]
out_file=sys.argv[2]
mode=0
if len(sys.argv)>3:
    mode=int(sys.argv[3])
    
if mode==1:
    tree=ET.parse(dat_file)
    root=tree.getroot()
    
    for content in root.findall('content'):
        print content.text
else:
    wiki=WikiCorpus(dat_file,lemmatize=False,dictionary=[])
    i=0
    with open(out_file,'w') as outf:
        for text in wiki.get_texts():
            outf.write(' '.join(text)+'\n')
            i+=1
            if i%10000==0:
                print 'Saved %d articles'%i
print 'finished'