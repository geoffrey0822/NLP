import caffe
import os,sys
import numpy as np
import leveldb
import subprocess as sp
import jieba
import subprocess

FFMPEG_BIN=os.environ['FFMPEG_BIN']

class AudioInputLayer(caffe.Layer):
    def setup(self,bottom,top):
        if FFMPEG_BIN == '' or FFMPEG_BIN is None:
            raise Exception('FFMPEG is undefined...')
        params=eval(self.param_str)
        self.annot_path=params['annotation_path']
        self.data_dir=params['data_dir']
        self.dict=''
        self.batch_size=1
        if 'batch_size' in params:
            self.batch_size=params['batch_size']
        self.length=0
        if 'length' in params:
            self.length=int(params['length'])
        self.word_len=0
        if 'word_length' in params:
            self.word_len=int(params['word_length'])
        self.word_dim=0
        if 'word_dim' in params:
            self.word_dim=int(params['word_dim'])
        self.isOneHot=False
        if 'is_onehot' in params and int(params['is_onehot'])==1:
            self.isOneHot=True
        if self.word_dim==0:
            print 'scan dictionary for obtaining information...',
            dict_db=leveldb.LevelDB(self.dict)
            for key,value in dict_db.RangeIter():
                self.word_dim+=1
            print '[Done]'
        self.word_dim+=1 # for padded
        self.shutil=False
        if 'shutil' in params:
            if params['shutil'] =='1':
                self.shutil=True
        self.total=0
        if 'total_size' in params:
            self.total=int(params['total_size'])
        self.isEncode=False
        if 'encoded' in params and int(params['encoded'])==1:
            self.isEncode=True
        else:
            self.dict=params['dict']
        tmp_word_length=0
        if self.total==0:
            print 'preparing for dataset...',
        db=leveldb.LevelDB(self.annot_path)
        if self.length>0:
            for key,value in db.RangeIter():
                self.total+=1
                if self.word_len==0:
                    params=value.split(';')
                    sentences=os.path.join(self.data_dir,params[1])
                    
        else:
            self.length=0
            for key,value in db.RangeIter():
                params=value.split(';')
                audio_file=os.path.join(self.data_dir,params[0])
                if os.path.isfile(audio_file):
                    cmd=[os.path.join(FFMPEG_BIN,'ffmpeg'),'-i',audio_file,'-f','wav','-']
                    p=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    data=p.communicate()[0]
                    npdata=np.fromstring(data[data.find('data')+4:],np.int16)
                    if self.length<len(npdata):
                        self.length=len(npdata)
                            
                    self.total+=1
            print 'Approx. length of data:%d'%self.length
            print '[Done]'
        self.channel=1
        self.height=1
        self.width=self.length
        self.idx=0
        
    def reshape(self,bottom,top):
        top[0].reshape(*[self.batch_size,self.channel,self.height,self.width])
        if self.isOneHot:
            top[1].reshape(*[self.batch_size,self.word_dim,self.word_len])
        else:
            top[1].reshape(*[self.batch_size,1,self.word_len])
    
    def forward(self,bottom,top):
        db=leveldb.LevelDB(self.annot_path)
        n=0
        
        while n< self.batch_size:
            data_row=db.Get(str(self.idx),default=None)
            if data_row is None:
                self.idx=0
                data_row=db.Get(str(self.idx),default=None)
            params=data_row.split(';')
            audio_file=os.path.join(self.data_dir,params[0])
            if os.path.isfile(audio_file):
                cmd=[os.path.join(FFMPEG_BIN,'ffmpeg'),'-i',audio_file,'-f','wav','-']
                p=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                data=p.communicate()[0]
                if data is None:
                    self.idx+=1
                    continue
                npdata=np.fromstring(data[data.find('data')+4:],np.int16)
                faudio=npdata.astype(np.float32,order='C')/32768.0
                paddedAudio=np.zeros((self.channel,self.height,self.length),dtype=np.float)
                gt_label=None
                words=params[1].lstrip().rstrip().split(' ')
                i=0
                if self.isOneHot:
                    gt_label=np.zeros((self.word_dim,self.word_len),dtype=np.float)
                    for word in words:
                        gt_label[int(word)+1,i]=1.0
                        i+=1
                    while i<self.word_len:
                        gt_label[0,i]=1.0
                        i+=1
                else:
                    gt_label=np.zeros((1,self.word_len),dtype=np.float)
                    for word in words:
                        gt_label[0,i]=int(word)+1
                        i+=1
                    while i<self.word_len:
                        gt_label[0,i]=0
                        i+=1
                paddedAudio[:,0,:len(faudio)]=faudio
                #print words
                
                top[0].data[n,...]=paddedAudio
                top[1].data[n,...]=gt_label
                n+=1
            self.idx+=1
            if self.idx>=self.total:
                self.idx=0
    
    def backward(self,top,propagate_down,bottom):
        pass