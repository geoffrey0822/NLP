import leveldb
import os,sys
import jieba
import base64

def append2Dict(db,words,last_idx=-1):
    if last_idx==-1:
        for key,val in db.RangeIter():
            idx=int(val)
            if last_idx<idx:
                last_idx=idx
        last_idx+=1
    for word in words:
        eword=base64.b64encode(word)
        val= db.Get(eword,default=None)
        if val is None:
            db.Put(eword,str(last_idx))
            last_idx+=1
    return last_idx

def encodeString(db,words):
    vect=' '
    for word in words:
        eword=base64.b64encode(word)
        idx=db.Get(eword,default=None)
        vect+=str(idx)+' '
    return vect.rstrip()

csv_path=sys.argv[1]
dst_path=sys.argv[2]
db_name=sys.argv[3]
encode=False
dict_path=''
has_title=False
isEnglish=True
if len(sys.argv)>4 and sys.argv[4]=='1':
    has_title=True
if len(sys.argv)>5 and sys.argv[5]=='1':
    encode=True
    dict_path=sys.argv[6]
    if len(sys.argv)>7 and sys.argv[7]=='0':
        isEnglish=False
        
        
if not os.path.isdir(dst_path):
    os.mkdir(dst_path)
    
db_path=os.path.join(dst_path,'%s.ldb'%db_name)
info_path=os.path.join(dst_path,'%s_info.txt'%db_name)
total=0
dict_db=None
word_dim=0
if dict_path!='':
    dict_db=leveldb.LevelDB(dict_path)
    for key,value in dict_db.RangeIter():
        if int(value)>word_dim:
            word_dim=int(value)
with open(csv_path,'r') as f:
    db=leveldb.LevelDB(db_path)
    i=0
    print 'Converting CSV...',
    last_idx=word_dim+1
    max_len=0
    for ln in f:
        i+=1
        line=ln.rstrip('\n')
        if i==1 and has_title:
            continue
        data_str=line.replace(',',';')
        if encode:
            fields=data_str.split(';')
            new_sentences=''
            if isEnglish:
                words=fields[1].split(' ')
                last_idx=append2Dict(dict_db, words, last_idx)
                new_sentences=encodeString(dict_db,words)
                if len(words)>max_len:
                    max_len=len(words)
            else:
                words=list(jieba.cut(fields[1],cut_all=False))
                last_idx=append2Dict(dict_db, words, last_idx)
                new_sentences=encodeString(dict_db,words)
                if len(words)>max_len:
                    max_len=len(words)
            fields[1]=new_sentences
            data_str=';'.join(fields)
            #print words
        db.Put(str(total),data_str)
        total+=1
        if total%10000==0:
            print '\rConverting CSV...saved %d records'%total,
with open(info_path,'w') as f:
    f.write('No.of data=%d\n'%total)
    f.write('dimension of word=%d\n'%last_idx)
    f.write('Max length of sentence=%d'%max_len)
print 'All Done'